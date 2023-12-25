import sqlite3


def run_script(filename):
    with open(filename, 'r') as f:
        sql = f.read()

    with sqlite3.connect('../university.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


if __name__ == "__main__":
    for i in range(1, 13):
        print(f'Result for query {i}:')
        result = run_script(f'query_{i}.sql')
        print(*result, sep='\n')
        print('----------------------------------------------------------------')
