import random
import time

import lib

con = lib.database.connect('database.db')
candidates = lib.database.get_candidates(con)

cur = con.cursor()

VOTES = 500

for i in range(VOTES):
	cur.execute("""INSERT INTO votes VALUES(?, ?)""", [random.choice(candidates)[1], time.time()])

con.commit()
