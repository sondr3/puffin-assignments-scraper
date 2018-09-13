import requests
import xlsxwriter
from bs4 import BeautifulSoup
from datastructures import *


def findNoPages(baseUrl=None, headers=None):
    assert baseUrl is not None
    assert headers is not None
    response = requests.get(baseUrl, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")

    lis = soup.find_all("li", {"class": "page-item"})
    return int(lis[3].text)



def getStudent(id=None, students=None):
    assert id is not None
    assert students is not None

    for student in students:
        if student.id == id:
            return student
    
    return None


def getAssignmentsFromOnePage(studentsList=None, baseUrl=None, pageNumber=None, headers=None):
    assert studentsList is not None
    assert pageNumber is not None
    assert baseUrl is not None
    assert headers is not None

    response = requests.get(baseUrl + "&page=" + str(pageNumber), headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    
    trs = soup.find_all("tr")

    for i in range(1, len(trs)):
        tds = trs[i].find_all("td")
        id = tds[0].text
        assignment = tds[1].text
        group = tds[2].text
        score = tds[3].text
        max = tds[4].text

        assignment = Assignment(group=group, assignment=assignment, score=score, max=max)

        student = getStudent(id=id, students=studentsList)

        if student is None:
            newStudent = Student(id=id)
            newStudent.addAssignment(assignment)
            studentsList.append(newStudent)
        else:
            student.addAssignment(assignment)

cookie = ""

baseUrl = "https://puffin.ii.uib.no/submissions/?category=&group=&assignment=&filtering=my-student"
headers = { 
    "Cookie": cookie
}

noPages = findNoPages(baseUrl=baseUrl, headers=headers)

students = list()

for i in range(noPages):
    getAssignmentsFromOnePage(studentsList=students, baseUrl=baseUrl, pageNumber=(i + 1), headers=headers)







workbook = xlsxwriter.Workbook('new.xlsx')
worksheet = workbook.add_worksheet()


for i in range(len(students)):
    
    worksheet.write(i, 0, students[i].id)
    weekly = students[i].getWeeklyExercises()

    for j in range(len(weekly)):
        a = weekly[j]
        worksheet.write(i, j + 1, (a))

workbook.close()