import time

import xlsxwriter

from utils import *

base_URL = "https://puffin.ii.uib.no/submissions/?category=&group=&assignment=&filtering=my-student&sort=-assignment__group__name"
profile_URL = "https://puffin.ii.uib.no/account/profile/"
cookie = ""
headers = {"Cookie": cookie}

students = list()
get_students(profile_URL, headers, students)
no_pages = find_no_pages(base_URL, headers)

for i in range(no_pages):
    get_assignments_from_one_page(students, base_URL, (i + 1), headers)

workbook = xlsxwriter.Workbook(str(time.time()) + ".xlsx")
worksheet = workbook.add_worksheet()

current_assignments = ["Assignment 0", "Assignment 1", "Assignment 2", "Assignment 3"]
data_area = (
    "C2:" + get_letter_index(len(current_assignments) + 2) + str(len(students) + 1)
)

worksheet.write(0, 0, len(students))

for i in range(len(current_assignments)):
    worksheet.write(0, i + 2, current_assignments[i])

for i in range(len(students)):
    current_student = students[i]
    worksheet.write(i + 1, 0, current_student.id)
    worksheet.write(i + 1, 1, current_student.name)

    for j in range(len(current_assignments)):
        assignment = current_assignments[j]
        student_score = current_student.get_exercise_score("Weekly", assignment)
        worksheet.write(i + 1, j + 2, student_score)

# Light red fill with dark red text.
format1 = workbook.add_format({"bg_color": "#FFC7CE", "font_color": "#9C0006"})

# Light yellow fill with dark yellow text.
format2 = workbook.add_format({"bg_color": "#FFEB9C", "font_color": "#9C6500"})

# Green fill with dark green text.
format3 = workbook.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})

worksheet.conditional_format(
    data_area,
    {
        "type": "cell",
        "criteria": "between",
        "minimum": 0.01,
        "maximum": 0.99,
        "format": format2,
    },
)

worksheet.conditional_format(
    data_area, {"type": "cell", "criteria": "equal to", "value": 1, "format": format3}
)

worksheet.conditional_format(
    data_area, {"type": "cell", "criteria": "equal to", "value": 0, "format": format1}
)

workbook.close()
