import subprocess
import json
import sys
import os


def install_packages():
    try:
        import pip
    except ImportError:
        print("ERROR: pip not present.\nInstalling pip...")
        exec(open("setup/get-pip.py").read())
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bottle', 'matplotlib', 'gunicorn'])


def generate_config():
    config = eval(open("setup/config_template.json").read(), {'input': input, '__builtins__': None})
    json_config = json.dumps(config, indent=4)

    with open("config.json", "w") as outfile:
        outfile.write(json_config)


def generate_database():
    import lib.database
    con = lib.database.connect("database.db")
    lib.database.setup(con)

    candidates = eval(open("setup/candidates.list").read(), {'__builtins__': None})
    lib.database.set_candidates(con, candidates)

    lib.database.set_admins(con, [(input("Enter admin username: "), input("Enter admin password: "))])
    lib.database.set_settings(con, [("voting_active", "0"), ("live_results", "0"), ("code_duration", "5")])
    print("NOTE: Voting is disabled now, but you can enable it on the admin panel. The candidates of 2023 are already set, but if you need other candidates you can set them there. Also dont forget to remove the disclaimer.")
    con.close()


if __name__ == "__main__":
    print("~~~~~ PYTHON PACKAGES ~~~~~")
    install_packages()

    print("~~~~~ CONFIG ~~~~~")
    if not os.path.exists(os.getcwd() + "/config.json"):
        generate_config()
    elif not input("An existing config was found. Do you want to overwrite it? (y/n): ") == "y":
        print("Skipping config")
        pass
    else:
        os.remove(os.getcwd() + "/config.json")
        generate_config()

    print("~~~~~ DATABASE ~~~~~")
    if not os.path.exists(os.getcwd() + "/database.db"):
        generate_database()
    elif not input("An existing database was found. Do you want to overwrite it? (y/n): ") == "y":
        print("Skipping database")
        pass
    else:
        os.remove(os.getcwd() + "/database.db")
        generate_database()

    print("~~~~~ STATIC FOLDER ~~~~~")
    try:
        os.mkdir(os.getcwd() + "/static/")
        print("DONE: creating folder /static/")
    except FileExistsError:
        print("ERROR: folder /static/ already exists")

    print("\nInstallation done. Check README.md for further information.")