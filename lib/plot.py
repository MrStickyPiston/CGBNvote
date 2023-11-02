import sys
import hashlib

import matplotlib.pyplot as plt

try:
    import lib.database
except ModuleNotFoundError:
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

    if not results:
        return 148

    results_hash = hashlib.sha512(repr(results).encode('utf-8')).hexdigest()

    if results_hash == open('static/results-hash.sha512', 'w+').read():
        # No changes
        return

    with open('static/results-hash.sha512', 'w') as f:
        f.write(results_hash)

    for result in results:
        votes.append(result[0])
        counts.append(result[1])

    print(votes)
    print(counts)

    party_count_pairs = list(zip(votes, counts))
    sorted_party_count_pairs = sorted(party_count_pairs, key=lambda x: x[1])

    sorted_votes = [pair[0] for pair in sorted_party_count_pairs]
    sorted_counts = [pair[1] for pair in sorted_party_count_pairs]

    con.commit()

    print("Plotting the results")
    plt.barh(sorted_votes, sorted_counts, color="#1e78b6")
    plt.xlabel('Aantal stemmen')
    plt.title('CGBNvote resultaten')

    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(base=1))

    plt.savefig('static/results.webp', bbox_inches="tight", )


if __name__ == "__main__":
    con = lib.database.connect("database.db")
    exit(plot_votes(con))
