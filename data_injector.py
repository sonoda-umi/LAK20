data_path = 'data/Train'
db_path = 'database/lak20.db'
import sqlite3
import csv
import os

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('''CREATE TABLE event_stream
             (user_id text,course_id text,material_id text,operation_name text,page_no real,marker text,memo_length real,devicecode text,eventtime text)''')
c.execute('''CREATE TABLE lecture_detail
             (course_id text, lecture_serial real, material_id text, material_pages real, start_time text,end_time text)''')
# conn.commit()


for filename in os.listdir(data_path):
    if filename.endswith("LectureMaterial.csv"):
        course_id = filename.split('_')[1]
        print(course_id)
        with open(os.path.join(data_path, filename), 'rt', encoding='utf-8') as material_file, open(
                os.path.join(data_path, 'Course_' + course_id + '_LectureTime.csv'), 'rt',
                encoding='utf-8') as time_file:
            lecture_data = []
            lecture_serial = []
            material_id = []
            material_pages = []
            start_time = []
            end_time = []
            material_reader = csv.reader(material_file)
            time_reader = csv.reader(time_file)
            next(material_reader, None)
            next(time_reader, None)
            for row in material_reader:
                lecture_serial.append(float(row[0]))
                material_id.append(row[1])
                material_pages.append(float(row[2]))
            for row in time_reader:
                start_time.append(row[0])
                end_time.append(row[1])
            for index in range(len(lecture_serial)):
                lecture_data.append((course_id, lecture_serial[index], material_id[index], material_pages[index],
                                     start_time[index], end_time[index]))
            c.executemany("INSERT INTO lecture_detail VALUES (?,?,?,?,?,?)", lecture_data)
    conn.commit()

for filename in os.listdir(data_path):
    if filename.endswith("EventStream.csv"):
        course_id = filename.split('_')[1]
        print(course_id)
        with open(os.path.join(data_path, filename), 'rt', encoding='utf-8') as event_stream_file:
            event_stream_file_reader = csv.reader(event_stream_file)
            next(event_stream_file_reader, None)
            for row in event_stream_file_reader:
                row.insert(0,course_id)
                print(row)
                c.execute("INSERT INTO event_stream VALUES (?,?,?,?,?,?,?,?,?)",row)
    conn.commit()

c.execute("SELECT COUNT(*) FROM event_stream")
print(c.fetchall())
