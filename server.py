import lib
import json, ctypes, os
try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

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
    if ssl_key != "None" and ssl_cert != "None":
        print("Using https")
        lib.web.serve_https(host, ssl_port, ssl_key, ssl_cert)
    else:
        print("Using http")
        lib.web.serve(host, port)
