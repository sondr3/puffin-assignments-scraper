import requests
from bs4 import BeautifulSoup

class Student:

    def __init__(self, id=None, name="No Name"):
        assert id is not None
        self.id = id
        self.name = name
        self.assignments = list()

    def addAssignment(self, assignment):
        self.assignments.append(assignment)

    def getWeeklyExercises(self):
        we = list()
        for a in self.assignments:
            if a.group == "Weekly":
                we.append(a)
        return we

    def getFirstAssignmentByName(self, name=None):
        assert name is not None
        for a in self.assignments:
            if a.assignment == name:
                return a
        return None

    def getWeeklyAssignmentByName(self, name=None):
        assert name is not None
        weeklyAssignments = self.getWeeklyExercises()
        for a in weeklyAssignments:
            if a.assignment == name:
                return a
        return None

    def getPercentScoreOfWeeklyAssignmentByName(self, name=None):
        assert name is not None
        assignment = self.getWeeklyAssignmentByName(name=name)
        if assignment is None:
            return 0
        if float(assignment.max) == float(assignment.score):
            return 1
        return (float(assignment.score) / float(assignment.max))

    def getFirstPercentScore(self, name=None):
        assert name is not None
        assignment = self.getFirstAssignmentByName(name=name)
        if assignment is None:
            return 0
        if float(assignment.max) == 0:
            return 1
        return (float(assignment.score) / float(assignment.max))

class Assignment:

    def __init__(self, group=None, assignment=None, score=None, max=None):
        assert group is not None
        assert assignment is not None
        assert score is not None
        assert max is not None

        self.group = group
        self.assignment = assignment
        self.score = score
        self.max = max

    def __str__(self):
        return (self.group + ": " + self.assignment)


def getStudent(id=None, students=None):
    assert id is not None
    assert students is not None

    for student in students:
        if student.id == id:
            return student
    
    return None

def findNoPages(baseUrl=None, headers=None):
    assert baseUrl is not None
    assert headers is not None
    response = requests.get(baseUrl, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")

    lis = soup.find_all("li", {"class": "page-item"})
    return int(lis[3].text)

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

        # print("id: ", id, ", assignment: ", assignment, " group: ", group)

        assignment = Assignment(group=group, assignment=assignment, score=score, max=max)

        student = getStudent(id=id, students=studentsList)


        if student is None:
            newStudent = Student(id=id)
            newStudent.addAssignment(assignment)
            studentsList.append(newStudent)
        else:
            student.addAssignment(assignment)

def getStudents(url=None, headers=None, studentsList=None):
    assert url is not None
    assert studentsList is not None
    assert headers is not None

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    lis = soup.find_all("li")
    noPages = int(lis[len(lis) - 2].text)

    for i in range(noPages):
        getStudentsFromPage(baseUrl=url, headers=headers, studentsList=studentsList, pageNumber=(i + 1))

def getStudentsFromPage(baseUrl=None, headers=None, studentsList=None, pageNumber=None):
    assert baseUrl is not None
    assert headers is not None
    assert studentsList is not None
    assert pageNumber is not None

    response = requests.get(baseUrl + "?student_page=" + str(pageNumber), headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")

    ls = soup.find("div", id="recommended_list")
    a = ls.find_all("a", {"data-toggle":"collapse"})

    for person in a:
        divs = person.find_all("div")
        newStudent = Student(id=divs[1].text, name=divs[0].text)
        studentsList.append(newStudent)


def getLetterIndex(i):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return letters[i - 1]