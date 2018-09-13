class Student:

    def __init__(self, id=None):
        assert id is not None
        self.id = id
        self.assignments = list()

    def addAssignment(self, assignment):
        self.assignments.append(assignment)

    def getWeeklyExercises(self):
        we = list()
        for a in self.assignments:
            if a.group == "Weekly":
                we.append(a.assignment)
        we.sort()
        return we

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


    