from dataclasses import dataclass, field
from typing import List

import requests
from bs4 import BeautifulSoup


def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item):
            return item


@dataclass
class Assignment:
    group: str
    assignment: str
    score: float
    max: float

    def __str__(self):
        return self.group + ": " + self.assignment

    def get_percentage_score(self):
        if float(self.max) == 0:
            return 1
        else:
            return float(self.score) / float(self.max)


def get_student(student_id, students):
    return find(lambda student: student.id == student_id, students)


def find_no_pages(base_url, headers):
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    lis = soup.find_all("li", {"class": "page-item"})
    return int(lis[3].text)


@dataclass
class Student:
    id: str = None
    name: str = "No name"
    book_exercises: List[Assignment] = field(default_factory=list)
    weekly_exercises: List[Assignment] = field(default_factory=list)

    def get_exercise_score(self, group, name):
        exercise = self.get_exercise(group, name)
        if exercise is None:
            return 0
        else:
            return exercise.get_percentage_score()

    def get_exercise(self, group, name):
        if group == "Weekly":
            return find(
                lambda exercise: exercise.assignment == name, self.weekly_exercises
            )
        else:
            return find(
                lambda exercise: exercise.assignment == name, self.book_exercises
            )

    def add_exercise(self, exercise):
        if exercise.group == "Weekly":
            self.weekly_exercises.append(exercise)
        else:
            self.book_exercises.append(exercise)


def get_assignments_from_one_page(students_list, base_url, page_number, headers):
    response = requests.get(base_url + "&page=" + str(page_number), headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    trs = soup.find_all("tr")
    for i in range(1, len(trs)):
        tds = trs[i].find_all("td")
        assignment_id = tds[0].text
        assignment = tds[1].text
        group = tds[2].text
        score = tds[3].text
        assignment_max = tds[4].text

        # print("id: ", id, ", assignment: ", assignment, " group: ", group)

        assignment = Assignment(group, assignment, score, assignment_max)
        student = get_student(assignment_id, students_list)

        if student is None:
            new_student = Student(id=assignment_id)
            students_list.append(new_student)
            new_student.add_exercise(assignment)
        else:
            student.add_exercise(assignment)


def get_students(url, headers, students_list):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    lis = soup.find_all("li")
    no_pages = int(lis[len(lis) - 2].text)
    for i in range(no_pages):
        get_students_from_page(url, headers, students_list, (i + 1))


def get_students_from_page(base_url, headers, students_list, page_number):
    response = requests.get(
        base_url + "?student_page=" + str(page_number), headers=headers
    )
    soup = BeautifulSoup(response.text, features="html.parser")
    ls = soup.find("div", id="recommended_list")
    a = ls.find_all("a", {"data-toggle": "collapse"})
    for person in a:
        divs = person.find_all("div")
        new_student = Student(id=divs[1].text, name=divs[0].text)
        students_list.append(new_student)


def get_letter_index(i):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return letters[i - 1]
