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
        else:
            port = data["port"]
except Exception:
    exit("Incorrect config file")

ssl_key = "None"
ssl_cert = "None"

if __name__ == '__main__':
    if ssl_key != "None" and ssl_cert != "None":
        print("Using https")
        lib.web.serve_https(host, port, ssl_cert, ssl_key)
    else:
        print("Using http")
        lib.web.serve(host, port)
