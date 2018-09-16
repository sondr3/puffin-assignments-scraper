import requests
from bs4 import BeautifulSoup


def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item):
            return item


class Student:

    def __init__(self, id=None, name="No Name"):
        assert id is not None
        self.id = id
        self.name = name
        self.bookExercises = list()
        self.weeklyExercises = list()

    def getExerciseScore(self, group, name):
        exercise = self.getExercise(group, name)
        if exercise is None:
            return 0
        else:
            return exercise.getPercentageScore()

    def getExercise(self, group, name):
        if group == "Weekly":
            return find(lambda exercise: exercise.assignment == name, self.weeklyExercises)
        else:
            return find(lambda exercise: exercise.assignment == name, self.bookExercises)

    def addExercise(self, exercise):
        if exercise.group == "Weekly":
            self.weeklyExercises.append(exercise)
        else:
            self.bookExercises.append(exercise)


class Assignment:

    def __init__(self, group, assignment, score, max):

        self.group = group
        self.assignment = assignment
        self.score = score
        self.max = max

    def __str__(self):
        return (self.group + ": " + self.assignment)

    def getPercentageScore(self):
        if float(self.max) == 0:
            return 1
        else:
            return float(self.score) / float(self.max)


def getStudent(id, students):
    return find(lambda student: student.id == id, students)


def findNoPages(baseUrl, headers):
    response = requests.get(baseUrl, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    lis = soup.find_all("li", {"class": "page-item"})
    return int(lis[3].text)


def getAssignmentsFromOnePage(studentsList, baseUrl, pageNumber, headers):
    response = requests.get(baseUrl + "&page=" +
                            str(pageNumber), headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    trs = soup.find_all("tr")
    for i in range(1, len(trs)):
        tds = trs[i].find_all("td")
        id = tds[0].text
        assignment = tds[1].text
        group = tds[2].text
        score = tds[3].text
        max = tds[4].text

        # print("id: ", id, ", assignment: ", assignment, " group: ", group)

        assignment = Assignment(group, assignment, score, max)
        student = getStudent(id, studentsList)

        if student is None:
            newStudent = Student(id=id)
            newStudent.addAssignment(assignment)
            studentsList.append(newStudent)
            newStudent.addExercise(assignment)
        else:
            student.addExercise(assignment)


def getStudents(url, headers, studentsList):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    lis = soup.find_all("li")
    noPages = int(lis[len(lis) - 2].text)
    for i in range(noPages):
        getStudentsFromPage(url, headers, studentsList, (i + 1))


def getStudentsFromPage(baseUrl, headers, studentsList, pageNumber):
    response = requests.get(baseUrl + "?student_page=" +
                            str(pageNumber), headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    ls = soup.find("div", id="recommended_list")
    a = ls.find_all("a", {"data-toggle": "collapse"})
    for person in a:
        divs = person.find_all("div")
        newStudent = Student(id=divs[1].text, name=divs[0].text)
        studentsList.append(newStudent)


def getLetterIndex(i):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return letters[i - 1]
