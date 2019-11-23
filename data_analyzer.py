import sqlite3
data_path = 'data/Train'
db_path = 'database/lak20.db'
course_id = '6b1900c56c'
material_id = 'e18eedce0b'

conn = sqlite3.connect(db_path)
c = conn.cursor()

sql = "SELECT * FROM event_stream where course_id='%s'"%course_id
print(sql)
c.execute(sql)
print(c.fetchall())

