import psycopg2, json
from psycopg2.extras import DictCursor, NamedTupleCursor

conn = psycopg2.connect(dbname='railway', user='postgres',
                        password='oWFn9Oa0KWOQeqTCCtP1', host='containers-us-west-75.railway.app', port = 7799)
cursor = conn.cursor(cursor_factory=NamedTupleCursor)
cursor.execute('SELECT * FROM parties LIMIT 10')
records = cursor.fetchall()
print(type(records))
for item in records:
    print(type(item), item[1])

# PGPASSWORD=oWFn9Oa0KWOQeqTCCtP1 psql -h containers-us-west-75.railway.app -U postgres -p 7799 -d railway
# postgresql://postgres:oWFn9Oa0KWOQeqTCCtP1@containers-us-west-75.railway.app:7799/railway
