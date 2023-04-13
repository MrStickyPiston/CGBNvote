import lib
import json, ctypes, os
try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

os.system('cls' if os.name=='nt' else 'clear')

try:
    with open("config.json", 'r') as file:
        data = json.load(file)

        host = data["ip"]
        if is_admin:
            port = data["admin_port"]
            ssl_port = data["ssl_admin_port"]
        else:
            port = data["port"]
            ssl_port = data["ssl_port"]

        ssl_key = data["ssl_key"]
        ssl_cert = data["ssl_cert"]

except Exception:
    exit("Incorrect config file")

if __name__ == '__main__':
    # Decide which server to use
    if os.name == 'nt':
        print("""
+------------------------------------------------------------+
| host: windows (not recommended)                            |
| server: waitress                                           |
| This not very unstable but migth not suppport all features |""")
        server = 'waitress'

    elif 'ANDROID_BOOTLOGO' in os.environ:
        print("""
+------------------------------------------------------------+
| host: Android (NOT RECOMMENDED)                            |
| server: bottle                                             |
| This should be for debug only.                             |
| YOU WILL NOT RECEIVE ANY SUPPORT.                          |
+------------------------------------------------------------+""")
        server = 'bottle'
        lib.web.serve(host, port, server)

    else:
        print("""
+------------------------------------------------------------+
| host: linux (recommended)                                  |
| server: gunicorn                                           |
| Ideal for hosting the prod server.                         |""")
        server = 'gunicorn'

    # Start the server
    if ssl_key != "None" and ssl_cert != "None":
        print("""| Mode: http                                                 |
+------------------------------------------------------------+""")
        lib.web.serve_https(host, ssl_port, server, ssl_key, ssl_cert)
    else:
        print("""| Mode: https                                                |
+------------------------------------------------------------+""")
        lib.web.serve(host, port, server)
