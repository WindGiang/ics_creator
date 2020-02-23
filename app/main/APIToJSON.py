# coding=utf-8
import json
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
        course_list = self.stu.getKbcx()
        print('已经爬取到json')
        print(course_list)

        for course_api in course_list:
            print(course_api)
            course['ClassName'] = course_api['kcmc']
            week['StartWeek'] = int(course_api['kkzc'].split('-')[0])
            week['EndWeek'] = int(course_api['kkzc'].split('-')[1])
            course['Week'] = week.copy()
            courseTime['Start'] = int(course_api['kcsj'][1:3])
            courseTime['End'] = int(course_api['kcsj'][-2:])
            course['ClassTime'] = courseTime.copy()
            course['ClassRoom'] = course_api['jsmc']
            course['Teacher'] = course_api['jsxm']
            course['Weekday'] = int(course_api['kcsj'][0])
            '''这里注意，将一个字典插入数组，只是一个字典地址送过去，如果我们对字典改动，那么数组里面的值也会变'''
            course_list_cov.append(course.copy())

        json_list['ClassInfo'] = course_list_cov
        with open(self.account + '.json', 'w+', encoding='utf-8') as j:
            j.write(json.dumps(json_list, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    jsonc = JsonCreator('username', 'password')
    jsonc.creatJson()
