import json
import secrets
import subprocess
import sys

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


def generate_database(admin_name, admin_password):
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

    password = admin_password
    validation = check_password(password)
    if not validation[0]:
        print(validation[1])
        return False

    database.set_admins(con, [(admin_name, admin_password)])
    database.set_settings(con, db_config)
    con.close()

    return True


def generate_config(server_url, server_mail, mail_password):
    config = eval(open("setup/templates/project_config.pyjson").read(),
                  {
                      '__builtins__': None,
                      'secrets': secrets,
                      'server_url': server_url,
                      'server_mail': server_mail,
                      'mail_password': mail_password
                  })
    json_config = json.dumps(config, indent=4)

    with open("config.json", "w") as outfile:
        outfile.write(json_config)


if __name__ == "__main__":
    install_packages()
    generate_config(
        input('server url: '),
        input('server email: '),
        input('server email password: ')
    )

    credentials = [input('admin name: '), input('admin password: ')]

    while not generate_database(credentials[0], credentials[1]):
        credentials[1] = input('admin password (safe): ')

    print('Run the server now')