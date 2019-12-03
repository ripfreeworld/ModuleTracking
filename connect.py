# This script is for connecting with PostgreSQL Database
import psycopg2
import sys

conn = None
cursor = None
try:
    conn = psycopg2.connect(database='jumpingjive', user='ge69zaq', password='jump', host='localhost', port='5432')
    cursor = conn.cursor()
    print('Connected...')


except psycopg2.DatabaseError as e:
    print('error code {}: {}'.format(e.pgcode, e))
    sys.exit(1)

conn.commit()