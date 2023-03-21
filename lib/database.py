import sqlite3, secrets, string, time


def connect(db):
    try:
        con = sqlite3.connect(db)
        return con
    except sqlite3.Error as e:
        print(e)


def setup(con):
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS auth(userid,
                                                   code, 
                                                   voted, 
                                                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
                                                   )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS votes(vote,
                                                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
                                                   )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS candidates(id,
                                                       displayname
                                                       )""")
    con.commit()


def generate_code(con, userid):
    cur = con.cursor()

    cur.execute("SELECT * FROM 'auth' WHERE userid = ?", [userid])
    existing = cur.fetchall()

    try:
        code = existing[0][1]
    except IndexError:
        code = "NULL"
    code_edited = False

    if len(existing) >= 1:
        if existing[0][2] == 1:
            pass
        else:
            # Generate a new code
            code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
            code_edited = True

            # Clone list and update existing values
            updated = list(existing[0])
            updated[1] = code
            updated[3] = time.time()
            cur.execute("""UPDATE auth
                        SET userid = ?,
                            code = ? ,
                            voted = ?,
                            timestamp = ?
                        WHERE userid = ?""", updated + [updated[0]])
    else:
        code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
        code_edited = True

        cur.execute("""
                    INSERT INTO auth VALUES(?, ?, False, ?)
                    """,
                    (userid, code, time.time()))
    con.commit()
    return [code, code_edited]


def disable_code(con, userid):
    cur = con.cursor()

    cur.execute("SELECT * FROM 'auth' WHERE userid = ?", [userid])
    existing = cur.fetchall()

    try:
        updated = list(existing[0])
    except IndexError:
        return "codeNotFoundException"

    updated[2] = 1
    cur.execute("""UPDATE auth
                SET userid = ?,
                    code = ? ,
                    voted = ?,
                    timestamp = ?
                WHERE userid = ?""", updated + [userid])
    con.commit()
    return "0"


def get_codes(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM 'auth'")
    db = cur.fetchall()
    return db


def set_candidates(con, candidates):
    cur = con.cursor()
    cur.execute("DELETE FROM 'candidates'")

    for i in candidates:
        cur.execute("""INSERT INTO candidates VALUES(?, ?)""", [i[0], i[1]])


def get_candidates(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM 'candidates'")
    db = cur.fetchall()
    con.commit()
    return db


def insert_vote(con, userid, code, vote):
    cur = con.cursor()
    candidates = get_candidates(con)

    cur.execute("SELECT * FROM 'auth' WHERE userid = ?", [userid])
    try:
        credentials = cur.fetchall()[0]
    except IndexError:
        return "notFoundException"

    print(candidates)

    if credentials[1] == code and int(credentials[3]) + 300 > time.time() and credentials[2] == 0:
        if vote in [i[1] for i in candidates]:
            disable_code(con, userid)
            cur.execute("""INSERT INTO votes VALUES(?, ?)""", [vote, time.time()])
        else:
            return "candidateException"
    else:
        return "authException"

    con.commit()
    return "success"


if __name__ == "__main__":
    con = connect("dev_database.db")
    setup(con)
    cur = con.cursor()

    set_candidates(con, [('Zweintje', 'zweintje'), ('Partij Voor de Varkens', 'pvv')])

    userid = "test2"
    code = generate_code(con, userid)

    print(insert_vote(con, "test2", code, "Zweintje"))
    con.close()
