class IDAllocator:
    def __init__(self):
        self._last_id = -1
    def new_id(self):
        return str(self._last_id + 1).zfill(4)

class Course:
    def __init__(self, department, code, semester, instructor=None, students=[]):
        self.department = department
        self.code = code
        self.semester = semester
        self.instructor = instructor
        self.students = students
    
    def add_student(self, student):
        self.students.append(student)

    def assign_instructor(self, instructor):
        self.instructor = instructor

    def name(self):
        return '{} {}'.format(self.department, self.code)

class Person:
    def __init__(self, user_id, first, last):
        self.first = first
        self.last = last
        self.id = user_id

    def full_name(self):
        return '{}, {}'.format(last, first)

class Student(Person):
    def __init__(self, user_id, first, last, courses, grades):
        super().__init__(user_id, first, last)
        self.courses = courses
    def courses_enrolled(self):
        return self.courses

class Admin(Person):
    '''
    Represents either an Instructor or Administrator
    '''
    def __init__(self, user_id, first, last):
        super().__init__(user_id, first, last)
