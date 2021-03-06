import requests
import xlsxwriter
from utils import *
import time

baseUrl = "https://puffin.ii.uib.no/submissions/?category=&group=&assignment=&filtering=my-student&sort=-assignment__group__name"
profileUrl = "https://puffin.ii.uib.no/account/profile/"
cookie = ""
headers = { "Cookie": cookie }

students = list()
getStudents(profileUrl, headers, students)
noPages = findNoPages(baseUrl, headers)

for i in range(noPages):
    getAssignmentsFromOnePage(students, baseUrl, (i + 1), headers)

workbook = xlsxwriter.Workbook(str(time.time()) + '.xlsx')
worksheet = workbook.add_worksheet()

currentAssignments = ["Assignment 0","Assignment 1","Assignment 2","Assignment 3"]
dataArea = "C2:" + getLetterIndex(len(currentAssignments) + 2) + str(len(students) + 1)

worksheet.write(0, 0, len(students))

for i in range(len(currentAssignments)):
    worksheet.write(0, i + 2, currentAssignments[i])

for i in range(len(students)):
    currentSudent = students[i]
    worksheet.write(i + 1, 0, currentSudent.id)
    worksheet.write(i + 1, 1, currentSudent.name)

    for j in range(len(currentAssignments)):
        assignment = currentAssignments[j]
        studentScore = currentSudent.getExerciseScore("Weekly", assignment)
        worksheet.write(i + 1, j + 2, studentScore)

# Light red fill with dark red text.
format1 = workbook.add_format({'bg_color':   '#FFC7CE',
                               'font_color': '#9C0006'})

# Light yellow fill with dark yellow text.
format2 = workbook.add_format({'bg_color':   '#FFEB9C',
                               'font_color': '#9C6500'})

# Green fill with dark green text.
format3 = workbook.add_format({'bg_color':   '#C6EFCE',
                               'font_color': '#006100'})


worksheet.conditional_format(dataArea, {'type': 'cell',
                                       'criteria': 'between',
                                       'minimum': 0.01,
                                       'maximum': 0.99,
                                       'format': format2})

worksheet.conditional_format(dataArea, {'type': 'cell',
                                       'criteria': 'equal to',
                                       'value': 1,
                                       'format': format3})

worksheet.conditional_format(dataArea, {'type': 'cell',
                                       'criteria': 'equal to',
                                       'value': 0,
                                       'format': format1})


workbook.close()