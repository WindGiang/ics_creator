# coding=utf-8
import json
import os

from QZ_API import SW

json_list = {}
course_list_cov = []
course = {}
week = {'StartWeek': 1, 'EndWeek': 1}
courseTime = {'Start': 1, 'End': 1}


class JsonCreator:
    def __init__(self, account, password):
        self.stu = SW(account, password)
        self.account = account

    def creatJson(self):
        if not self.stu.isLogin:
            return
        course_list = self.stu.getKbcx()
        print('已经爬取到json')
        for course_api in course_list:
            course['ClassName'] = course_api['kcmc']
            courseTime['Start'] = int(course_api['kcsj'][1:3])
            courseTime['End'] = int(course_api['kcsj'][-2:])
            course['ClassTime'] = courseTime.copy()
            course['ClassRoom'] = course_api['jsmc']
            course['Teacher'] = course_api['jsxm']
            course['Weekday'] = int(course_api['kcsj'][0])
            '''这里注意，将一个字典插入数组，只是一个字典地址送过去，如果我们对字典改动，那么数组里面的值也会变'''
            if ',' in course_api['kkzc']:
                courseweeklist = course_api['kkzc'].split(',')
                for courseweek in courseweeklist:
                    if '-' in courseweek:
                        week['StartWeek'] = int(courseweek.split('-')[0])
                        week['EndWeek'] = int(courseweek.split('-')[1])
                        course['Week'] = week.copy()
                        course_list_cov.append(course.copy())
                    else:
                        week['StartWeek'] = int(courseweek)
                        week['EndWeek'] = int(courseweek)
                        course['Week'] = week.copy()
                        course_list_cov.append(course.copy())
            else:
                if '-' in course_api['kkzc']:
                    week['StartWeek'] = int(course_api['kkzc'].split('-')[0])
                    week['EndWeek'] = int(course_api['kkzc'].split('-')[1])
                    course['Week'] = week.copy()
                    course_list_cov.append(course.copy())
                else:
                    week['StartWeek'] = int(course_api['kkzc'])
                    week['EndWeek'] = int(course_api['kkzc'])
                    course['Week'] = week.copy()
                    course_list_cov.append(course.copy())

        json_list['ClassInfo'] = course_list_cov
        with open(os.path.abspath('cache/json/'+self.account + '.json'), 'w+', encoding='utf-8') as j:
            j.write(json.dumps(json_list, indent=4, ensure_ascii=False))
