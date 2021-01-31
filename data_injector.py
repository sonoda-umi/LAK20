from pathlib import Path

import sqlite3
import csv
import os


data_dir_path = 'data'
db_dir_path = 'database'
db_file = 'database.db'
db_path = os.path.join(db_dir_path,db_file)
Path(db_dir_path).mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS event_stream;''')
c.execute('''DROP TABLE IF EXISTS lecture_detail;''')
c.execute('''CREATE TABLE event_stream
             (course_id text,user_id text,material_id text,operation_name text,page_no real,marker text,memo_length real,devicecode text,eventtime text)''')
c.execute('''CREATE TABLE lecture_detail
             (course_id text, lecture_serial text, material_id text, material_pages real, start_time text,end_time text)''')
# conn.commit()


for filename in os.listdir(data_dir_path):
    if filename.endswith(".csv"):
        with open(os.path.join(data_dir_path, filename), 'rt', encoding='utf-8') as course_log:

            # Lecture detail list dec
            lecture_data = []
            lecture_serial = []
            material_id = []
            material_pages = []
            start_time = []
            end_time = []
            course_id = []

            # Event Stream list dec
            event_data = []
            user_id = []
            operation_name = []
            page_no = []
            marker = []
            device_code =[]
            event_time = []

            material_reader = csv.reader(course_log)
            next(material_reader, None)
            for row in material_reader:
                # Lecture detail app
                course_id.append(row[0])
                lecture_serial.append(row[3])
                material_id.append(row[12])
                material_pages.append(9999)
                start_time.append(row[19])
                end_time.append(row[20])
                # Event Stream app
                user_id.append(row[2])
                operation_name.append(row[10])
                page_no.append(row[17])
                marker.append(row[16])
                device_code.append(row[14])
                event_time.append(row[19])

            for index in range(len(lecture_serial)):
                lecture_data.append((course_id[index], lecture_serial[index], material_id[index], material_pages[index],
                                     start_time[index], end_time[index]))
                event_data.append((course_id[index],user_id[index],material_id[index],operation_name[index],page_no[index],marker[index],0,device_code[index],event_time[index]))
            c.executemany("INSERT INTO lecture_detail VALUES (?,?,?,?,?,?)", lecture_data)
            c.executemany("INSERT INTO event_stream VALUES (?,?,?,?,?,?,?,?,?)",event_data)
    conn.commit()

# for filename in os.listdir(data_dir_path):
#     if filename.endswith("EventStream.csv"):
#         course_id = filename.split('_')[1]
#         print(course_id)
#         with open(os.path.join(data_dir_path, filename), 'rt', encoding='utf-8') as event_stream_file:
#             event_stream_file_reader = csv.reader(event_stream_file)
#             next(event_stream_file_reader, None)
#             for row in event_stream_file_reader:
#                 row.insert(0,course_id)
#                 print(row)
#                 c.execute("INSERT INTO event_stream VALUES (?,?,?,?,?,?,?,?,?)",row)
#     conn.commit()

c.execute("SELECT COUNT(*) FROM event_stream")
print(c.fetchall())
