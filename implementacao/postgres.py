import psycopg2

conn = psycopg2.connect(host='localhost', database="python_des", user="postgres", password="123456")
cur = conn.cursor()

sql = 'select * from tb001_servidor'

cur.execute(sql)

#print cur.fetchone()

#print cur.fetchall()

for servidor in cur:
	print servidor[0]

cur.close()
conn.close()

