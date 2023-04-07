import subprocess
import json
import sys
import os


def install_packages():
    try:
        import pip
    except ImportError:
        print("ERROR: pip not present.\nInstalling pip...")
        exec(open("get-pip.py").read())
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bottle', 'matplotlib', 'gunicorn'])


def generate_config():

    default_config = {
        "ip": "0.0.0.0",
        "port": "8080",
        "admin_port": "80",

        "ssl_port": "8443",
        "ssl_admin_port": "443",
        "ssl_key": "None",
        "ssl_cert": "None",

        "url": input("Enter the server url: "),
        "mail": input("Enter server mail adress: "),
        "mail_password": input("Enter mail (app)password: ")
    }
    json_config = json.dumps(default_config, indent=4)

    with open("config.json", "w") as outfile:
        outfile.write(json_config)


def generate_database():
    import lib

    con = lib.database.connect("database.db")
    lib.database.setup(con)

    lib.database.set_candidates(con,
                                [
                                 ('DISCLAIMER:', 'Deze partijen komen van de lijst "Nationaal vertegenwoordigd" op wikipedia op 07-04-2023'),
                                 ('Volkspartij voor Vrijheid en Democratie', 'vvd'),
                                 ('Democraten 66', 'd66'),
                                 ('Partij voor de Vrijheid', 'pvv'),
                                 ('Christen-Democratisch Appèl', 'cda'),
                                 ('Socialistische Partij', 'sp'),
                                 ('Partij van de Arbeid', 'pvda'),
                                 ('GroenLinks', 'gl'),
                                 ('Partij voor de Dieren ', 'pvdd'),
                                 ('ChristenUnie', 'cu'),
                                 ('Forum voor Democratie', 'fvd'),
                                 ('JA21', 'ja21'),
                                 ('Staatkundig Gereformeerde Partij', 'sgp'),
                                 ('DENK', 'denk'),
                                 ('Volt Nederland', 'volt'),
                                 ('BoerBurgerBeweging', 'bbb'),
                                 ('BIJ1', 'bij1'),
                                 ('50PLUS', '50plus'),
                                 ('Onafhankelijke Politiek Nederland', 'opnl')
                                 ])

    lib.database.set_admins(con, [(input("Enter admin username: "), input("Enter admin password: "))])
    lib.database.set_settings(con, [("voting_active", "0"), ("live_results", "0"), ("code_duration", "5")])
    print("NOTE: Voting is disabled now, but you can enable it on the admin panel. You can also edit the candidates there.")
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