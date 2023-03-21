import lib

host = "localhost"
port = 8080

if __name__ == '__main__':
    con = lib.database.connect("database.db")
    lib.database.setup(con)
    lib.database.set_candidates(con, [('Zweintje', 'zweintje'), ('Partij Voor de Varkens', 'pvv')])

    print(f"""Candidates: {lib.database.get_candidates(con)}""")

    con.close()

    lib.web.serve(host, port)
