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
        print(f"""
+------------------------------------------------------------+
| host:     windows (not really recommended)                 |
| server:   waitress                                         |
| workers:  {2*os.cpu_count()}                                               |""")
        server = 'waitress'

    elif 'ANDROID_BOOTLOGO' in os.environ:
        print("""
+------------------------------------------------------------+
| host: Android (NOT RECOMMENDED)                            |
| server: bottle                                             |
| workers: 1                                                 |
| workers: 1                                                 |
| This should be for debug only.                             |
| YOU WILL NOT RECEIVE ANY SUPPORT.                          |
+------------------------------------------------------------+""")
        lib.web.serve_bottle(host, port)
        exit()

    else:
        print(f"""
+------------------------------------------------------------+
| host:     linux (recommended)                              |
| server:   gunicorn                                         |
| workers:  {2*os.cpu_count()}                                               |""")
        server = 'gunicorn'

    # Start the server
    if ssl_key != "None" and ssl_cert != "None":
        print("""| Mode:     https                                            |
+------------------------------------------------------------+""")
        lib.web.serve_https(host, ssl_port, server, 2*os.cpu_count(), ssl_key, ssl_cert)
    else:
        print("""| Mode:     http                                             |
+------------------------------------------------------------+""")
        lib.web.serve_http(host, port, server, 2 * os.cpu_count())
