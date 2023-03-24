import sqlite3
import matplotlib.pyplot as plt

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

    for result in results:
        votes.append(result[0])
        counts.append(result[1])

    con.commit()

    plt.bar(votes, counts)
    plt.ylabel('Aantal stemmen')
    plt.title('CGBNvote resultaten')

    plt.savefig('static/results.webp')