import sqlite3
# import data_analyzer
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

db_path = 'database/database.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT DISTINCT material_id FROM event_stream")
material_list = c.fetchall()
for material_id in material_list:
    c.execute("SELECT DISTINCT course_id FROM event_stream WHERE material_id = '%s'" % material_id)
    course_list = c.fetchall()
    for course_id in course_list:
        print(material_id[0] + "_" + course_id[0])
        # poly_arr, max_app_arr = data_analyzer.polynomial_fitter(material_id[0], course_id[0], 100, 100, False, False)

        # Get event stream again
        event_stream = pd.read_sql(
            "SELECT page_no,user_id,eventtime FROM event_stream where material_id ='%s' and course_id='%s'" % (
                material_id[0], course_id[0]), conn)
        c.execute(
            "SELECT * FROM lecture_detail where material_id='%s' and course_id='%s'" % (material_id[0], course_id[0]))
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
        fig1 = plt.figure(figsize=(15, 10))
        app_list = np.zeros(int(page_count))
        # reference_arr = max_app_arr

        threshold = 2
        duration_threshold = 20

        for std_event in in_class_event_stream.groupby('user_id'):
            valid_pages = np.zeros(int(page_count))

            # ax1 = fig1.add_subplot(111)
            # ax1.set_title("%s_%s" % (material_id, course_id))
            # ax1.plot(std_event[1]['operation_time'], std_event[1]['page_no'], color="#3592C4")
            # ax1.plot(op_time_list, max_app_arr, color="red")

            page_no_list = std_event[1]['page_no'].to_numpy()
            operation_time_list = std_event[1]['operation_time'].to_numpy()
            counting = False
            is_started = False
            start_index = 0
            for index in range(len(page_no_list)):
                page_loc = page_no_list[index]
                op_time = operation_time_list[index]
                if counting:
                    if False:
                        pass
                    # if page_loc >= reference_arr[int(op_time) - 1] - threshold:
                    #     counting = False
                    else:
                        # Do the counting in page array
                        if 0 < index < len(page_no_list) - 1:
                            # Confirm it's not the first and last in list
                            if page_loc == page_no_list[index - 1] and page_loc == page_no_list[index + 1]:
                                # Do nothing for middle item
                                pass
                            if page_loc != page_no_list[index - 1]:
                                # This is start item
                                # TODO: record the staring point
                                start_index = index
                                is_started = True
                                pass
                            if page_loc != page_no_list[index + 1]:
                                # This is ending item
                                # TODO: calculate the duration and record
                                if is_started:
                                    duration = operation_time_list[index + 1] - op_time_list[start_index]
                                    if duration > duration_threshold:
                                        valid_pages[int(page_no_list[index]) - 1] += 1
                                    is_started = False
                                pass
                            else:
                                print("This is unhandled situation with index on:")
                                print(index)
                        pass
                else:
                    if True:
                    # if page_loc < reference_arr[int(op_time) - 1] - threshold:
                        counting = True
            print(valid_pages)
            app_list += valid_pages
        ax1 = fig1.add_subplot(111)
        ax1.set_title("%s_%s" % (material_id, course_id))
        ax1.plot(range(1,int(page_count)+1),app_list)
        plt.show()
            # text = np.array2string(valid_pages)
            # plt.text(4, 1, text, wrap=True)
            # plt.savefig(datetime.datetime.now().strftime("%H-%M-%S-%f") + ".png")
            #plt.show()

