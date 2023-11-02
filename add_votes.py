import random
import time

import lib

con = lib.database.connect('database.db')
candidates = lib.database.get_candidates(con)

cur = con.cursor()

for i in candidates:
	if random.randint(0, 2) > 1:
		cur.execute("""INSERT INTO votes VALUES(?, ?)""", [i[1], time.time()])

con.commit()
