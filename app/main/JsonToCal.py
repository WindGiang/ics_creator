import json
import os
import uuid
from operator import eq

from icalendar import Calendar, Event, Timezone, Alarm, TimezoneStandard
from datetime import datetime, timedelta
from pytz import timezone, utc
from flask import make_response,send_file

FirstWeekDate = datetime(2020, 2, 17, 00, 00, 00, tzinfo=timezone("Asia/Shanghai"))
daylight_date = datetime(2020, month=5, day=1, hour=0, minute=0, tzinfo=timezone('Asia/Shanghai'))
standard_date = datetime(2020, month=10, day=1, hour=0, minute=0, tzinfo=timezone('Asia/Shanghai'))
timedelta_stand = daylight_date - FirstWeekDate
week_length = int(timedelta_stand.days / 7) + 1  # 表示第几周第几天之前是标准时间，其余是夏令时 对于本学期来说
day_length = int(timedelta_stand.days % 7)

with open(os.path.abspath('app/static/Json/Timetable.json'), 'r') as timejson:
    time_table = json.load(timejson)
    timejson.close()


class Course:

    def __init__(self, c_name, start_week, end_week, c_teacher, c_weekday, start_class, end_class, classroom, time_zone,
                 step=1):
        self.time_zone = time_zone
        self.step = step
        self.classroom = classroom
        self.end_class = end_class
        self.start_class = start_class
        self.c_weekday = c_weekday
        self.c_teacher = c_teacher
        self.end_week = end_week
        self.start_week = start_week
        self.c_name = c_name

    def getStartTime(self, time_):
        Day = int(self.start_week - 1) * 7 + int(self.c_weekday) - 1
        Hour = int(time_table[time_][str(self.start_class)]['start'] / 100)
        Minute = int(time_table[time_][str(self.start_class)]['start'] % 100)
        return FirstWeekDate + timedelta(days=Day, hours=Hour, minutes=Minute)

    def getEndTime(self, time_):
        Day = int(self.start_week - 1) * 7 + int(self.c_weekday) - 1
        Hour = int(time_table[time_][str(self.end_class)]['end'] / 100)
        print(Hour)
        Minute = int(time_table[time_][str(self.end_class)]['end'] % 100)
        print(Minute)
        return FirstWeekDate + timedelta(days=Day, hours=Hour, minutes=Minute)

    def getDescription(self):
        if self.time_zone == 'Standard':
            return str(
                '课程名称：' + self.c_name + ' 老师：' + self.c_teacher + ' 教室位置：' + self.classroom +
                ' 第' + str(self.start_week) + '-' + str(self.end_week) + '周' + ' 冬令时')
        else:
            return str(
                '课程名称：' + self.c_name + ' 老师：' + self.c_teacher + ' 教室位置：' + self.classroom +
                ' 第' + str(self.start_week) + '-' + str(self.end_week) + '周' + ' 夏令时')

    def getEvent(self):
        event = Event()
        event.add('summary', self.c_name)
        event.add('dtstart', self.getStartTime(self.time_zone))
        event.add('dtend', self.getEndTime(self.time_zone))
        event.add('dtstamp', datetime.now(tz=utc))
        event.add('location', self.classroom + ' ' + self.c_teacher)
        event['uid'] = str(uuid.uuid4())
        event.add('rrule',
                  {'freq': 'weekly', 'interval': str(self.step), 'count': str(self.end_week - self.start_week + 1)})
        event.add('description', self.getDescription())
        return event


def JsonLoadHandle(filename):
    week_length_real = 1
    jf = open(os.path.abspath('cache/json/'+filename+'.json'), 'r')
    text = json.load(jf)
    jf.close()
    flag = []
    for i in range(len(text['ClassInfo']) - 1):
        for j in range(i + 1, len(text['ClassInfo'])):
            if eq(text['ClassInfo'][i], text['ClassInfo'][j]):
                flag.append(int(j))
    for del_index in flag[::-1]:
        del text['ClassInfo'][del_index]
    course_list = []
    for item in text['ClassInfo']:
        if item['Week']['StartWeek'] <= week_length <= item['Week']['EndWeek']:
            if item['Weekday'] <= day_length:
                week_length_real = week_length
            elif item['Weekday'] > day_length:
                week_length_real = week_length - 1

            course_item = Course(item['ClassName'], item['Week']['StartWeek'], week_length_real,
                                 item['Teacher'], item['Weekday'], item['ClassTime']['Start'],
                                 item['ClassTime']['End'], item['ClassRoom'], 'Standard')
            if item['Week']['StartWeek'] <= week_length_real:
                course_list.append(course_item)
            course_item = Course(item['ClassName'], week_length_real + 1, item['Week']['EndWeek'],
                                 item['Teacher'], item['Weekday'], item['ClassTime']['Start'],
                                 item['ClassTime']['End'], item['ClassRoom'], 'Daylight')
            if week_length_real + 1 <= item['Week']['EndWeek']:
                course_list.append(course_item)
        elif item['Week']['StartWeek'] > week_length:
            course_item = Course(item['ClassName'], item['Week']['StartWeek'], item['Week']['EndWeek'],
                                 item['Teacher'], item['Weekday'], item['ClassTime']['Start'],
                                 item['ClassTime']['End'], item['ClassRoom'], 'Daylight')
            course_list.append(course_item)
        elif item['Week']['EndWeek'] < week_length:
            course_item = Course(item['ClassName'], item['Week']['StartWeek'], item['Week']['EndWeek'],
                                 item['Teacher'], item['Weekday'], item['ClassTime']['Start'],
                                 item['ClassTime']['End'], item['ClassRoom'], 'Standard')
            course_list.append(course_item)
    return course_list


def ical_creat(filename):
    courselist = JsonLoadHandle(filename)
    cal = Calendar()
    cal.add('prodid', '-//My CourseTable//')
    cal.add('version', '2.0')
    cal.add('CALSCALE', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    tz = Timezone()
    tzst = TimezoneStandard()
    tzst.add('tzoffsetfrom', timedelta(hours=8))
    tzst.add('tzoffsetto', timedelta(hours=8))
    tzst.add('tzname', 'CST')
    tzst.add('dtstart', datetime(1970, 1, 1, 0, 0, 0))
    tz.add('tzid', 'Asia/Shanghai')
    tz.add_component(tzst)
    cal.add_component(tz)
    for course in courselist:
        cal.add_component(course.getEvent())
    f = open(os.path.abspath('cache/ics/' + filename + '.ics'), 'wb')
    f.write(cal.to_ical())
    f.close()
    response = make_response(send_file(os.path.abspath('cache/ics/' + filename + '.ics')))
    response.headers["Content-Disposition"] = "attachment; filename=CourseTable-2019-2020-2.ics;"
    return response
