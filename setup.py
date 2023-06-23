import json
import os
import secrets
import subprocess
import sys
import threading
import time
import webbrowser

global _start_server

"""Checks if the correct python interpreter is being used.
Format: 3.11.3 = 3011003"""
version = sys.version_info.major * 1000000 + sys.version_info.minor * 1000 + sys.version_info.micro

if not sys.maxsize > 2 ** 32:
    exit("Invalid python interpreter: use 64 bit python instead.")
elif version < 3011000:
    exit(f"Invalid python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
         "\nCGBNvote requires at least python 3.11")


def install_packages():
    try:
        import pip
        print("Pip has been located.\nNot installing pip.")
    except ImportError:
        print("ERROR: pip not present.\nInstalling pip...")
        subprocess.check_call([sys.executable, 'setup/get-pip.py'])
        print("installed pip")

    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bottle', 'matplotlib', 'gunicorn', 'waitress'])


def generate_database():
    from lib import database
    def check_password(password):
        SpecialSym = """!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"""
        valid = True
        problems = ""

        if len(password) < 6:
            problems += ' Passsword length should be at least 6,'
            valid = False

        if not any(char.isdigit() for char in password):
            problems += ' Password should have at least one numeral,'
            valid = False

        if not any(char.isupper() for char in password):
            problems += ' Password should have at least one uppercase letter,'
            valid = False

        if not any(char.islower() for char in password):
            problems += ' Password should have at least one lowercase letter,'
            valid = False

        if not any(char in SpecialSym for char in password):
            problems += ' Password should have at least one special character,'
            valid = False

        if valid:
            return [valid]
        else:
            return [valid, problems[:-1]]

    con = database.connect("database.db")
    database.setup(con)

    candidates = eval(open("setup/templates/candidates.list").read(), {'__builtins__': None})
    db_config = eval(open("setup/templates/settings.list").read(), {'__builtins__': None})

    database.set_candidates(con, candidates)

    password = bottle.request.forms["password"]
    validation = check_password(password)
    if not validation[0]:
        return bottle.template("script", {"script": f"alert('Incorrect password: {validation[1]}'); history.back()"})

    database.set_admins(con, [(bottle.request.forms["user"], password)])
    database.set_settings(con, db_config)
    con.close()


def generate_config():
    config = eval(open("setup/templates/project_config.pyjson").read(), {'bottle': bottle,
                                                                         '__builtins__': None,
                                                                         'secrets': secrets})
    json_config = json.dumps(config, indent=4)

    with open("config.json", "w") as outfile:
        outfile.write(json_config)


if __name__ == "__main__":
    install_packages()

import bottle


class CloseAbleServer(bottle.ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass

            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        print("stopped setup server")
        self.server.shutdown()


@bottle.get('/')
def setup_form():
    return bottle.template("setup_form")


@bottle.post('/')
def setup_form():
    config_response = generate_config()
    database_response = generate_database()

    if config_response is not None:
        return config_response
    elif database_response is not None:
        return database_response

    try:
        os.mkdir(os.getcwd() + "/static/")
        print("Created folder /static/")
    except FileExistsError:
        pass

    if os.name == "nt":
        startup = "<p class=text>Uw wijzigingen zijn verwerkt.</p>" \
                  "</br><button class='button' id='iidnf' onclick=\"window.location.href = '/start-server';\">" \
                  "start server</button>"
    else:
        startup = "<p class=text>Uw wijzigingen zijn verwerkt. " \
                  "Start de server en klik daarna hieronder voor het admin panel</p>" \
                  "</br><button class='button' id='iidnf' onclick=\"window.location.href = '/admin-panel';\">Admin " \
                  "panel</button>"

        global _start_server
        _start_server = False

        def close_current():
            time.sleep(5)
            server.stop()

        close_thread = threading.Thread(target=close_current, daemon=True)
        close_thread.start()

    return bottle.template("setup_base", {"content": f"{startup}"})


@bottle.get('/start-server')
def start_server():
    def close_current():
        time.sleep(5)
        server.stop()

    close_thread = threading.Thread(target=close_current, daemon=True)
    close_thread.start()

    global _start_server
    _start_server = True

    return bottle.template("custom", {
        "content": "De server is opgestart. Klik <a href='/admin-panel'>hier</a> voor het admin-panel"})


webbrowser.open("http://127.0.0.1:8080")

server = CloseAbleServer()
bottle.run(server=server)

if _start_server:
    print("Starting server")
    import server

    server.main()
