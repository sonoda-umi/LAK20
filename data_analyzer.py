import sqlite3
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import numpy as np

# data_path = 'data/Train'
db_path = 'database/database.db'


def polynomial_fitter(material_id, course_id, start_variance, cut_down_variance,is_plot,is_save):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    event_stream = pd.read_sql(
        "SELECT page_no,user_id,eventtime FROM event_stream where material_id ='%s' and course_id='%s'" % (
            material_id, course_id),
        conn)
    c.execute("SELECT * FROM lecture_detail where material_id='%s' and course_id='%s'" % (material_id, course_id))
    lecture_details = c.fetchone()
    event_stream['eventtime'] = pd.to_datetime(event_stream['eventtime'])
    print(lecture_details)
    start_time = lecture_details[4]
    end_time = lecture_details[5]
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    mask = (event_stream['eventtime'] >= start_time) & (event_stream['eventtime'] <= end_time)
    in_class_event_stream = event_stream.loc[mask]
    in_class_event_stream['operation_time'] = (in_class_event_stream['eventtime'] - start_time).dt.total_seconds()

    # in_class_event_stream.set_index('operation_time', inplace=True)
    color = '#3592C4'
    fig1 = plt.figure(figsize=(15, 10))
    ax1 = fig1.add_subplot(111)
    ax1.set_title("%s_%s" % (material_id, course_id))

    max_op_time = (end_time - start_time).total_seconds()
    in_class_event_stream = in_class_event_stream.astype({"operation_time": int})
    op_time_list = list(range(int(max_op_time + 1)))
    stepped_event_stream = pd.DataFrame()
    for row in in_class_event_stream.groupby('user_id'):
        df = pd.DataFrame({"operation_time": op_time_list})
        df = df.astype({"operation_time": int})
        user_frame = row[1]
        user_frame.drop_duplicates(subset="operation_time", keep="last", inplace=True)
        user_frame = user_frame.astype({"operation_time": int})
        result = df.join(user_frame.set_index('operation_time'), on='operation_time')
        result = result.fillna(method="ffill")
        ax1.plot(result['operation_time'], result['page_no'], color=color, alpha=0.3)
        stepped_event_stream = stepped_event_stream.append(result)
    stepped_event_stream = stepped_event_stream.fillna(0)
    threshold = 1000
    data_list = []
    variance_list = []
    for row in stepped_event_stream.groupby('operation_time'):
        op_time = row[0]
        max_appear_value = row[1]['page_no'].value_counts().idxmax()
        mean = row[1]['page_no'].mean()
        variance = row[1]['page_no'].var()
        if variance > cut_down_variance:
            pass
        if variance > threshold:
            selected_value = mean
        else:
            selected_value = max_appear_value
        data_list.append((op_time, max_appear_value, mean, variance, selected_value))

    stat_df = pd.DataFrame(data_list,
                           columns=['operation_time', 'max_appearance', 'mean', 'variance', 'selected_value'])
    max_app = stat_df['max_appearance'].to_numpy()
    y = stat_df['selected_value'].to_numpy()
    x = stat_df['operation_time'].to_numpy()
    Loss_list = []
    for i in range(1, 30):
        Loss = 0
        Max_app_loss = 0
        z = np.polyfit(x, y, i)
        p = np.poly1d(z)
        for row in stepped_event_stream.groupby('operation_time'):
            mean = row[1]['page_no'].mean()
            Loss += abs(mean - p(row[0]))
            # print(row[0])
            Max_app_loss += abs(mean - max_app[row[0]])
        print("Power @ %d, Loss @ %f" % (i, Loss))
        print("Maximum Appearance loss @ %f" % Max_app_loss)
        Loss_list.append(Loss)
    minimum_loss = Loss_list.index(min(Loss_list)) + 1
    z = np.polyfit(x, y, minimum_loss)
    p = np.poly1d(z)
    ax1.plot(x, p(x), label=str(minimum_loss))
    ax1.plot(x, max_app[x], label="Max_Appearance")
    print(Loss_list)
    print("The minimum loss power is:%d" % (Loss_list.index(min(Loss_list)) + 1))
    ax1.legend()
    if is_save:
        plt.savefig("%s_%s.png" % (material_id, course_id))
    if is_plot:
        plt.show()
    return z,max_app


polynomial_fitter('e18eedce0b', '24a65f29b6', 100, 100,False,True)
