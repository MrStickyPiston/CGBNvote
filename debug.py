import lib

host = "0.0.0.0"
port = 8080

if __name__ == '__main__':
    con = lib.database.connect("database.db")
    lib.database.setup(con)
    lib.database.set_setting(con, "voting_active", False)
    lib.web.serve(host, port)

