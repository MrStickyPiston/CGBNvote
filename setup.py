import json
import secrets
import subprocess
import sys

import lib


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

    con = lib.database.connect("database.db")
    lib.database.setup(con)

    candidates = eval(open("setup/templates/candidates.list").read(), {'__builtins__': None})
    db_config = eval(open("setup/templates/settings.list").read(), {'__builtins__': None})

    lib.database.set_candidates(con, candidates)

    password = bottle.request.forms["password"]
    validation = check_password(password)
    if not validation[0]:
        return bottle.template("script", {"script": f"alert('Incorrect password: {validation[1]}'); history.back()"})

    lib.database.set_admins(con, [(bottle.request.forms["user"], password)])
    lib.database.set_settings(con, db_config)
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
        print("ERROR: folder /static/ already exists")

    subprocess.Popen([sys.executable, "server.py"])

    return bottle.template("custom", {"content": "NOTE: Voting is disabled now, but you can enable it on the <a href='/admin-panel'>admin panel</a>. The candidates of 2023 are already set, but if you need other candidates you can set them there. Also dont forget to remove the disclaimer."})


bottle.run()
