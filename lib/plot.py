import math
import pathlib
import sys
import hashlib
import os

import matplotlib.pyplot as plt

try:
	import lib.database
except ModuleNotFoundError:
	os.chdir(sys.argv[1])
	sys.path.append(sys.argv[1])
	import lib.database


def plot_votes(con):
	cur = con.cursor()

	query = '''
            SELECT vote, COUNT(*)
            FROM votes
            GROUP BY vote
        '''
	cur.execute(query)

	votes = []
	counts = []
	results = cur.fetchall()

	print(f'Vote results: {results}')
	if not results:
		return 148

	results_hash = hashlib.sha512(repr(results).encode('utf-8')).hexdigest()

	pathlib.Path.touch(pathlib.Path('static/results-hash.sha512'))

	# No changes
	if results_hash == open('static/results-hash.sha512', 'r').read() and os.path.exists('static/results.webp'):
		print('Bar chart already plotted for this votes')
		return

	with open('static/results-hash.sha512', 'w') as f:
		pass
		f.write(results_hash)

	for result in results:
		votes.append(result[0])
		counts.append(result[1])

	party_count_pairs = list(zip(votes, counts))
	sorted_party_count_pairs = sorted(party_count_pairs, key=lambda x: x[1])

	sorted_votes = [pair[0] for pair in sorted_party_count_pairs]
	sorted_counts = [pair[1] for pair in sorted_party_count_pairs]

	con.commit()

	print("Plotting the results")
	plt.barh(sorted_votes, sorted_counts, color="#1e78b6")
	plt.xlabel('Aantal stemmen')
	plt.title('CGBNvote resultaten')

	tick_space = math.ceil(max(sorted_counts) / 10)

	plt.gca().xaxis.set_major_locator(plt.MultipleLocator(base=tick_space))

	plt.savefig('static/results.webp', bbox_inches="tight", dpi=300)


if __name__ == "__main__":
	con = lib.database.connect("database.db")
	exit(plot_votes(con))
