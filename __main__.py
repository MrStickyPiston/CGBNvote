import lib

host = "0.0.0.0"
port = 8080

if __name__ == '__main__':
    con = lib.database.connect("database.db")
    lib.database.setup(con)
    lib.database.set_candidates(con, [('Volkspartij voor Vrijheid en Democratie', 'vvd'),
                                      ('Democraten 66', 'd66'),
                                      ('Partij voor de Vrijheid', 'pvv'),
                                      ('Christen-Democratisch Appèl', 'cda'),
                                      ('Socialistische Partij', 'sp')])
    lib.database.set_admins(con, [("sticky", "HelloWorld")])
    print(f"""Candidates: {lib.database.get_candidates(con)}""")

    con.close()

    lib.web.serve(host, port)
