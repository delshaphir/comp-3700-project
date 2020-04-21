
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
        
        # Skip first row (headers)
        return data[1:]

class Validator():

    # Access levels
    STUDENT_ACCESS = 0
    PARENT_ACCESS = 1
    INSTRUCTOR_ACCESS = 2
    ADMIN_ACCESS = 3

    def __init__(self, database):
        # Database (.csv file) to use for validation
        self.database = database

    def validate(self, email):
        '''
        Upon login success, searches for a user in the database
        and returns a Privileges object corresponding to their privileges.
        '''
        validation_data = DatabaseReader().read(self.database)
        user_row = [row for row in validation_data if row[1] == email][0]
        user_id = user_row[0]
        access_level = int(user_row[4])
        students = user_row[5].split(',')
        courses = user_row[6].split(',')
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

        return user_id, priv

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
        self.last_action = self.start # time of last session action
        self.SESSION_LIMIT = 3000 # amount of time (seconds) after which session should expire
        self.privileges = privileges

    def expired(self):
        '''
        Checks whether the session has expired. Also updates last_action
        '''
        now = dt.datetime.now()
        diff = now - self.last_action
        self.last_action = now
        if diff.days > 0:
            return True
        time_elapsed = diff.seconds
        return time_elapsed > self.SESSION_LIMIT

    def access_level(self):
        return self.privileges.level()
