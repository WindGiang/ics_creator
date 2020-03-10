import re
import sys
import json
import xlrd


def excel_to_json(filename):
    data = xlrd.open_workbook('/cache/excel/学生个人课表.xls')
    table = data.sheets()[0]
    ClassNameList = []
    TeacherNameList = []
    WeekList = []
    ClassWeekList = []
    ClassTimeList = []
    ClassRoomList = []
    for i in range(3, 9):
        for j in range(1, 8):
            DataLength = 0
            CellData = str(table.cell(i, j).value).split()
            DataLength = len(CellData)
            while DataLength != 0:
                ClassNameList.append(CellData[0])
                TeacherNameList.append(CellData[1])
                WeekList.append(CellData[2])
                ClassRoomList.append(CellData[3])
                ClassTimeList.append(CellData[4])
                ClassWeekList.append(j)
                DataLength -= 5
                if DataLength != 0:
                    CellData = CellData[5:]
    ClassInfo = '{\n"ClassInfo":[\n'
    pattern = re.compile(r'^[0-9]+-[0-9]+')

    for i in range(len(ClassNameList)):
        print(ClassTimeList[i][1:3])
        print(ClassTimeList[i][-4:-2])
        Week = pattern.search(WeekList[i]).group(0).split('-')
        ItemInfo = '{\n'
        ItemInfo += '"ClassName":"' + ClassNameList[i] + '",\n'
        ItemInfo += '"Week":{\n"StartWeek":' + Week[0] + ',\n'
        ItemInfo += '"EndWeek":' + Week[1] + '},\n'
        ItemInfo += '"Weekday":' + str(ClassWeekList[i]) + ',\n'
        ItemInfo += '"ClassTime":{\n"Start":' + str(int(ClassTimeList[i][1:3])) + ',\n'
        ItemInfo += '"End":' + str(int(ClassTimeList[i][-4:-2])) + '},\n'
        ItemInfo += '"ClassRoom":"' + ClassRoomList[i] + '",\n'
        ItemInfo += '"Teacher":"' + TeacherNameList[i] + '"\n' + '\n}'
        ClassInfo += ItemInfo
        if i != len(ClassNameList) - 1:
            ClassInfo += ","
    ClassInfo += ']\n}'
    with open('/Users/windgiang/PycharmProjects/icsCreator/cache/json/'+filename+'.json', 'w+') as f:
        f.write(ClassInfo)
        f.close()
    print("done!")
