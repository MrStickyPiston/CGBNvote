import subprocess
import json
import sys
import os

if __name__ == "__main__":
    # Packages
    print("~~~~~ PACKAGES ~~~~~")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bottle', 'matplotlib', 'gunicorn'])
    print("DONE: installing packages")

    # Config
    print("~~~~~ CONFIG ~~~~~")
    defaultconfig = {
        "ip": "0.0.0.0",
        "port": "8080",
        "admin_port": "80",
        "url": input("Enter the server url: "),
        "mail": input("Enter server mail adress: "),
        "mail_password": input("Enter mail password: ")
    }
    json_config = json.dumps(defaultconfig, indent=4)

    with open("config.json", "w") as outfile:
        outfile.write(json_config)

    print("DONE: generating config.json")

    try:
        os.mkdir(os.getcwd() + "/static/")
        print("DONE: creating folder /static/")
    except FileExistsError:
        print("ERROR: folder /static/ already exists")

    # Database
    print("~~~~~ DATABASE ~~~~~")
    import lib
    con = lib.database.connect("database.db")
    lib.database.setup(con)

    lib.database.set_candidates(con, [('Volkspartij voor Vrijheid en Democratie', 'vvd'),
                                      ('Democraten 66', 'd66'),
                                      ('Partij voor de Vrijheid', 'pvv'),
                                      ('Christen-Democratisch Appèl', 'cda'),
                                      ('Socialistische Partij', 'sp')])
    lib.database.set_admins(con, [(input("Enter admin username: "), input("Enter admin password: "))])
    lib.database.set_settings(con, [("voting_active", "0"), ("live_results", "0")])
    print("DONE: setting up database")
    print("NOTE: Voting is disabled now, but you can enable it on the admin panel. You can also edit the candidates there.")

    print("\nInstallation done. Check README.txt for further information.")

    con.close()
