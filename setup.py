import subprocess
import json
import sys
import os
import math


def header(message, char="=", charamount=-1, whitespace=0):
    if charamount == -1:
        charamount = int(math.ceil((100 - len(message)) / 2))
    return "\n" * whitespace + charamount * char + " " + message + " " + charamount * char


def install_packages():
    print(header("pip", char="~"))
    try:
        import pip
        print("Pip has been located.\nNot installing pip.")
    except ImportError:
        print("ERROR: pip not present.\nInstalling pip...")
        exec(open("setup/get-pip.py").read())

    print(header("installing packages", char="~"))
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bottle', 'matplotlib', 'gunicorn', 'waitress'])


def generate_config():
    config = eval(open("setup/config_template.json").read(), {'input': input, '__builtins__': None})
    json_config = json.dumps(config, indent=4)

    with open("config.json", "w") as outfile:
        outfile.write(json_config)


def generate_database():
    def check_password(password):
        SpecialSym = ['$', '@', '#', '%', "_"]
        valid = True

        if len(password) < 6:
            print('Passsword length should be at least 6')
            valid = False

        if not any(char.isdigit() for char in password):
            print('Password should have at least one numeral')
            valid = False

        if not any(char.isupper() for char in password):
            print('Password should have at least one uppercase letter')
            valid = False

        if not any(char.islower() for char in password):
            print('Password should have at least one lowercase letter')
            valid = False

        if not any(char in SpecialSym for char in password):
            print('Password should have at least one of the symbols $@#%_')
            valid = False
        if valid:
            return valid

    def get_password():
        password = input("Enter a admin password: ")
        while not check_password(password):
            password = input("Enter a strong admin password: ")
        return password

    con = lib.database.connect("database.db")
    lib.database.setup(con)

    candidates = eval(open("setup/candidates.list").read(), {'__builtins__': None})
    lib.database.set_candidates(con, candidates)

    lib.database.set_admins(con, [(input("Enter admin username: "), get_password())])
    lib.database.set_settings(con, [("voting_active", "0"), ("live_results", "0"), ("code_duration", "5")])
    print(
        "NOTE: Voting is disabled now, but you can enable it on the admin panel. The candidates of 2023 are already set, but if you need other candidates you can set them there. Also dont forget to remove the disclaimer.")
    con.close()


if __name__ == "__main__":
    print(header("PYTHON PACKAGES"))
    install_packages()

    print(header("CONFIGURATION"))
    if not os.path.exists(os.getcwd() + "/config.json"):
        # project configuration for new config
        print(header("CGBNvote instance configuration", char="~"))
        generate_config()

    elif not input("An existing config was found. Do you want to overwrite it? (y/n): ") == "y":
        print("Skipping config")
        pass

    else:
        # project configuration for existing config
        print(header("CGBNvote instance configuration", char="~"))
        os.remove(os.getcwd() + "/config.json")
        generate_config()

    # Check the database exists for later so that lib.web won't throw a mail exception.
    db_exists = os.path.exists(os.getcwd() + "/database.db")
    import lib

    if not db_exists:
        print(header("admin configuration", char="~"))
        generate_database()
    elif not input("\nAn existing database was found. Do you want to overwrite it? (y/n): ") == "y":
        print("Skipping database")
        pass
    else:
        print(header("admin configuration", char="~"))
        os.remove(os.getcwd() + "/database.db")
        generate_database()
    print("")

    print(header("static files folder", char="~"))
    try:
        os.mkdir(os.getcwd() + "/static/")
        print("Created folder /static/")
    except FileExistsError:
        print("ERROR: folder /static/ already exists")

    print("\nInstallation done. Check README.md for further information.")
