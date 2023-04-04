import csv
from collections import defaultdict

# 登録情報を取得
isPrivate = False
isEvent = False
myClass = []
with open('登録情報.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            isPrivate = row[1]
        elif i == 1:
            isEvent = row[1]
        else:
            myClass.append(row[1])

# 時間割の辞書を作成
timeTable_dict = defaultdict(list)
with open('./src/時間割.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        timeTable_dict[row[0]] = {'startTime': row[1], 'endTime': row[2]}

# 授業カレンダーの辞書を作成
classCalendar_dict = defaultdict(list)
with open('./src/授業カレンダー.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        date = row[0]
        day_of_week = row[1]
        if 1 <= int(row[2]) <= 14:
            classCalendar_dict[day_of_week].append(date)

# カレンダーに追加する内容を作成
contents = []
for classNum in myClass:
    with open('./src/syllabus.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for list in reader:
            if list[2] == classNum:
                subject = list[0]
                first_semester = True if '【学期前半】' in subject else False
                second_semester = True if '【学期後半】' in subject else False
                description = f'実施形態: {list[8]}\nシラバスURL:\n{list[14]}'
                class_times = list[10].split(',')
                for class_time in class_times:
                    day_of_week = class_time[0:1]
                    period = class_time[1:2]
                    semester = 0
                    if first_semester:
                        semester = 1
                    elif second_semester:
                        semester = 2
                    for i, date in enumerate(classCalendar_dict[day_of_week]):
                        if semester == 0 or (semester == 1 and i <= 7) or (semester == 2 and i >= 8):
                            content = {
                                'subject': subject,
                                'start_date': date,
                                'start_time': timeTable_dict[period]['startTime'],
                                'end_date': date,
                                'end_time': timeTable_dict[period]['endTime'],
                                'all_day_event': False,
                                'description': description
                            }
                            contents.append(content)

# CSVファイルに書き込み
header = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'All Day Event', 'Description', 'Location', 'Private']
with open('カレンダー追加.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for content in contents:
        writer.writerow([content['subject'], content['start_date'], content['start_time'], content['end_date'], content['end_time'], content['all_day_event'], content['description'], '', isPrivate])