import ctypes
import json
import math
import os
import socket
import sys
import urllib.request

import lib

try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

os.system('cls' if os.name == 'nt' else 'clear')

# Ping cloudflare to check for internet
try:
    socket.setdefaulttimeout(3)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("1.1.1.1", 443))
except socket.error as e:
    print(e)
    exit("No Wi-Fi acces available. Check your connection or try wired internet.")

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

        server_email = data["mail"]
        mail_domain = data["mail_domain"]

        threads = data["workers_per_core"] * os.cpu_count() + 1

except Exception:
    exit("Incorrect config file")

"""Checks if the correct python interpreter is being used.
Format: 3.11.3 = 3011003"""
version = sys.version_info.major * 1000000 + sys.version_info.minor * 1000 + sys.version_info.micro

if not sys.maxsize > 2 ** 32:
    exit("Invalid python interpreter: use 64 bit python instead.")
elif version < 3011000:
    exit(f"Invalid python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
         "\nCGBNvote requires at least python 3.11")

protocol = "https" if ssl_key != "None" and ssl_cert != "None" else "http"
external_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
internal_ip = s.getsockname()[0]


class ServerInfo:
    def __init__(self, title="", space=5, width=20):
        self.title = title.strip()
        self.space = space

        self.width = width
        self.info = []

    def text(self, id, value=None):
        if value is None:
            self.info.append(f"{id}")
        else:
            self.info.append(f"{id}: {value}")

        if len(self.info[-1]) > self.width:
            self.width = len(self.info[-1])

    def section(self, name="None", space=True):
        self.info.append(f"NEW_SECTION:{name}:{space}")

    def render(self,
               left_top="┌",
               top="─",
               right_top="┐",
               left_bottom="└",
               bottom="─",
               right_bottom="┘",
               side="│",
               left_seperator="├",
               seperator="─",
               right_seperator="┤"):
        render = f"{left_top}{top * (math.floor(0.2 * (self.width + 2 + self.space)) - 1)}" \
                 f" {self.title} " \
                 f"{top * (math.ceil(0.8 * (self.width + 2 + self.space)) - 1 - len(self.title))}{right_top}\n"

        for i in self.info:
            if i.startswith("NEW_SECTION:"):
                title = i.split(':')[1]

                if i.split(':')[2] == "True":
                    render += f"{side} {' ' * (self.width + self.space)} {side}\n"

                if title != "None":
                    render += \
                        f"{left_seperator}{seperator * (math.floor(0.2 * (self.width + 2 + self.space)) - 1)}" \
                        f" {title} " \
                        f"{top * (math.ceil(0.8 * (self.width + 2 + self.space)) - 1 - len(title))}{right_seperator}\n"
                else:
                    render += f"{left_seperator}{seperator * (self.width + self.space + 2)}{right_seperator}\n"

            else:
                render += f"{side} {i}{' ' * (self.width - len(i) + self.space)} {side}\n"

        render += f"{side} {' ' * (self.width + self.space)} {side}\n"
        render += f"{left_bottom}{bottom * (self.width + 2 + self.space)}{right_bottom}\n"

        return render


def main():
    info = ServerInfo("CGBNvote server info", 10, 60)

    if os.name == 'nt':
        server = 'waitress'
        operating_system = "Windows (Not recommended)"

    elif 'ANDROID_BOOTLOGO' in os.environ:
        server = 'bottle'

        info.text("Host OS", "Android (NOT RECOMMENDED)")
        info.text("Server", f"{server} ({1} thread)")
        info.text("Host ip", f"{host}:{port}")
        info.text("")
        info.text("Only do this if you know what you are doing")
        info.text("YOU WILL NOT RECEIVE ANY SUPPORT.")

        print(info.render())
        lib.web.serve_bottle(host, port)
        exit()

    else:
        server = 'gunicorn'
        operating_system = "Linux (Recommended)"

    info.text("OS", operating_system)
    info.text("Server", f"{server} ({threads} threads)")

    info.section("Connections")
    info.text("Protocol", protocol)
    info.text("Host", host)
    info.text("Port", port)
    info.text("")
    info.text("LAN", f"{protocol}://{internal_ip}:{port}")
    info.text("Public", f"{protocol}://{external_ip}:{port}")

    info.section("Mail")
    info.text("Server email", server_email)
    info.text("Server email authenticated", not lib.web.disable_mail)
    info.text("User mail extension", f"@{mail_domain}")

    print(info.render())

    if protocol == "https":
        lib.web.serve_https(host, ssl_port, server, threads, ssl_key, ssl_cert)
    else:
        lib.web.serve_http(host, port, server, threads)


if __name__ == '__main__':
    main()
