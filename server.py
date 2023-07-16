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

# Ping google to check for internet
try:
    socket.setdefaulttimeout(3)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("8.8.8.8", 53))
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

        threads = data["workers_per_core"] * os.cpu_count()

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

    def add(self, name, value=None):
        if value is None:
            self.info.append(f"{name}")
        else:
            self.info.append(f"{name}: {value}")

        if len(self.info[-1]) > self.width:
            self.width = len(self.info[-1])

    def render(self, corner="+", top="-", bottom="-", side="|"):
        render = f"{corner}{top * (math.floor(0.5 * (self.width - len(self.title) + 2 + self.space)) - 1)}" \
                 f" {self.title} " \
                 f"{top * (math.ceil(0.5 * (self.width - len(self.title) + 2 + self.space)) - 1)}{corner}\n"

        for i in self.info:
            render += f"{side} {i}{' ' * (self.width - len(i) + self.space)} {side}\n"

        render += f"{corner}{bottom * (self.width + 2 + self.space)}{corner}\n"

        return render


def main():
    info = ServerInfo("CGBNvote")

    if os.name == 'nt':
        server = 'waitress'
        operating_system = "Host OS", "Windows (Not recommended)"

    elif 'ANDROID_BOOTLOGO' in os.environ:
        server = 'bottle'

        info.add("Host OS", "Android (NOT RECOMMENDED)")
        info.add("Server", f"{server} ({1} thread)")
        info.add("Host ip", f"{host}:{port}")
        info.add("")
        info.add("Only do this if you know what you are doing")
        info.add("YOU WILL NOT RECEIVE ANY SUPPORT.")

        print(info.render())
        lib.web.serve_bottle(host, port)
        exit()

    else:
        server = 'gunicorn'
        operating_system = "Linux (Recommended)"

    info.add("Host OS", operating_system)
    info.add("Server", f"{server} ({threads} threads)")

    info.add("Connections")
    info.add("Hosting on", f"{protocol}://{host}:{port}")
    info.add("LAN", f"{protocol}://{internal_ip}:{port}")
    info.add("Public", f"{protocol}://{external_ip}:{port}")

    print(info.render())

    if protocol == "https":
        lib.web.serve_https(host, ssl_port, server, threads, ssl_key, ssl_cert)
    else:
        lib.web.serve_http(host, port, server, threads)


if __name__ == '__main__':
    main()
