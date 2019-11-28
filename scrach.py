import sqlite3
import data_analyzer

db_path = 'database/lak20.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT DISTINCT material_id FROM event_stream")
material_list = c.fetchall()
for material_id in material_list:
    c.execute("SELECT DISTINCT course_id FROM event_stream WHERE material_id = '%s'" % material_id)
    course_list = c.fetchall()
    for course_id in course_list:
        print(material_id[0] + "_" + course_id[0])
        data_analyzer.polynomial_fitter(material_id[0], course_id[0],100,100)
