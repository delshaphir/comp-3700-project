import datetime as dt
import csv

class DatabaseReader():
    def __init__(self):
        pass
    
    def read(self, filename):
        data = []
        with open(filename, mode='r') as f:
            csvreader = csv.reader(f, dialect='excel')        
            for row in csvreader:
                data.append(row)
        return data


class Validator():

    # Access levels
    STUDENT_ACCESS = 0
    PARENT_ACCESS = 1
    INSTRUCTOR_ACCESS = 2
    ADMIN_ACCESS = 3

    def __init__(self, database):
        # Database (.csv file) to use for validation
        self.database = database

    def validate(self, user_id):
        '''
        Upon login success, searches for a user in the database
        and returns a Privileges object corresponding to their privileges.
        '''
        data = DatabaseReader().read(self.database)
        user_row = [row for row in data if int(row[0]) == user_id][0]
        access_level = int(user_row[3])
        students = user_row[4].split(',')
        courses = user_row[5].split(',')
        priv = None
        
        # Students cannot manage other students or courses
        if access_level == self.STUDENT_ACCESS:
            priv = Privilege(access_level)
            
        # Parents each manage one or more students
        elif access_level == self.PARENT_ACCESS:
            priv = Privilege(access_level, students=students)
            
        # Instructors manage courses. Administrators manage courses and *all* instructors
        elif access_level == self.INSTRUCTOR_ACCESS or access_level == self.ADMIN_ACCESS:
            priv = Privilege(access_level, courses=courses)

        return priv

class Privilege():
    def __init__(self, level, students=[], courses=[]):
        '''
        Represents a user's access level and holds
        which things they can access. Should be considered immutable.
        '''
        self._level = level
        self._students = students
        self._courses = courses

    def level(self):
        return self._level
    
    def can_manage_student(self, target_id):
        '''
        Returns whether the user can manage a student with the given ID.
        '''
        return any(student.id == target_id for student in self._students)

    def can_manage_course(self, target_name):
        '''
        Returns whether the user can manage a course with the given ID.
        '''
        return any(course.name() == target_name for course in self._courses)
    
    def courses(self):
        return self._courses
    def students(self):
        return self._students

class Session():
    def __init__(self, privileges):
        self.start = dt.datetime.now() # time of session creation
        self.SESSION_LIMIT = 10 # amount of time after which session should expire
        self.privileges = privileges
    
    def time_elapsed(self, start, end):
        '''
        Returns the time (in minutes) elapsed between two times
        '''
        diff = end - start
        secs_in_day = 86400
        return diff.days * secs_in_day / 60

    def expired(self):
        '''
        Returns whether the sesison has expired
        '''
        current_time = dt.datetime.now()
        return self.time_elapsed(self.start, current_time) > self.SESSION_LIMIT

    def access_level(self):
        return self.privileges.level()
