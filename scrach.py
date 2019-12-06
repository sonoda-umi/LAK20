import sqlite3
# import data_analyzer
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
        # poly_arr, max_app_arr = data_analyzer.polynomial_fitter(material_id[0], course_id[0], 100, 100)

        # Get event stream again
        event_stream = pd.read_sql(
            "SELECT page_no,user_id,eventtime FROM event_stream where material_id ='%s' and course_id='%s'" % (
            material_id[0], course_id[0]), conn)
        c.execute("SELECT * FROM lecture_detail where material_id='%s' and course_id='%s'" % (material_id[0], course_id[0]))
        lecture_details = c.fetchone()
        event_stream['eventtime'] = pd.to_datetime(event_stream['eventtime'])
        start_time = lecture_details[4]
        end_time = lecture_details[5]
        page_count = int(lecture_details[3])
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        mask = (event_stream['eventtime'] >= start_time) & (event_stream['eventtime'] <= end_time)
        in_class_event_stream = event_stream.loc[mask]
        in_class_event_stream['operation_time'] = (in_class_event_stream['eventtime'] - start_time).dt.total_seconds()

        max_op_time = (end_time - start_time).total_seconds()
        in_class_event_stream = in_class_event_stream.astype({"operation_time": int})
        op_time_list = list(range(int(max_op_time + 1)))

        reference_arr = np.zeros(int(max_op_time))
        for std_event in in_class_event_stream.groupby('user_id'):
            counting = False
            for index,row in std_event[1].iterrows():
                page_loc = row['page_no']
                op_time = row['operation_time']
            break


        color = '#3592C4'
        fig1 = plt.figure(figsize=(15, 10))
        ax1 = fig1.add_subplot(111)
        ax1.set_title("%s_%s" % (material_id, course_id))
        break
    break
