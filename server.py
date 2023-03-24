import lib

host = "0.0.0.0"
port = 80

if __name__ == '__main__':
    lib.web.serve(host, port)
