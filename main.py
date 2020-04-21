from student_system.validator import Validator, Privilege, Session
import student_system.controllers as control
from getpass import getpass
from typing import List
import sys

class StudentInformationSystem():

    # Databases
    db_path_stem = 'database/'
    db = {
        'login': 'logins.csv',
        'students': 'students.csv',
        'courses': 'courses.csv',
    }

    def __init__(self):
        self.validator = Validator(self.db_path_stem + self.db['login'])
        user_id, priv = self.login()
        if priv is None:
            print('Invalid user.')
            sys.exit()
        self.session = Session(user_id, priv)

        # Controllers
        self.student_control = control.StudentController(self.db_path_stem + self.db['students'])
        self.course_control = control.CourseController(self.db_path_stem + self.db['courses'])
        self.admin_control = control.AdminController(self.db_path_stem + self.db['login'])

    def start(self):
        print('Welcome to the Student Information System')
        self.menu()
        print('You have been logged out of the Student Information System.')

    def login(self):
        email = input('Email address: ')
        pwd = getpass('Password: ')
        return self.validator.validate(email)

    def menu(self):
        print() # empty line
        options = [
            ('Access Student controls', self.student_menu),
            ('Access Parent controls', self.parent_menu),
            ('Access Instructor controls', self.instructor_menu),
            ('Access Administrator controls', self.admin_menu),
            ('Log out', lambda: -1)
        ]
        choice = self.prompt_options(options)
        ret = options[choice][1]()
        if ret == 0:
            self.menu()
        return

    def student_menu(self):
        '''
        Show options for a student.
        '''
        access_level = self.session.access_level()
        if access_level != Validator.STUDENT_ACCESS:
            print('You must be a student to access this menu.')
            return 0
        view_student_data = lambda: self.student_control.view_student_data(self.session.user_id)
        options = [
            ('View student data', view_student_data),
            ('Return', lambda: 0)
        ]
        choice = self.prompt_options(options)
        return options[choice][1]()

    def parent_menu(self):
        '''
        Show options for a parent.
        '''
        access_level = self.session.access_level()
        if access_level != Validator.PARENT_ACCESS:
            print('You must be a parent to access this menu.')
            return 0
        view_student_data = lambda: self.student_control.view_student_data_by_name(
            self.admin_control.find_student(self.session.user_id))
        options = [
            ('View student data', view_student_data),
            ('Return', lambda: 0)
        ]
        choice = self.prompt_options(options)
        return options[choice][1]()

    def instructor_menu(self):
        '''
        Show options for an instructor.
        '''
        access_level = self.session.access_level()
        if access_level != Validator.INSTRUCTOR_ACCESS:
            print('You must be an instructor to access this menu.')
            return 0
        return -1

    def admin_menu(self):
        '''
        Show options for an administrator.
        '''
        access_level = self.session.access_level()
        if access_level != Validator.ADMIN_ACCESS:
            print('You must be an administrator to access this menu.')
            return 0
        print('Welcome to the Administrator menu.')
        assign_course = lambda: self.course_control.assign_instructor(self.admin_control.find_instructor())
        options = [
            ('Create a course', self.course_control.add_course),
            ('Assign a course to an instructor', assign_course),
            ('Return', lambda: 0)
        ]
        choice = self.prompt_options(options)
        return options[choice][1]()

    def prompt_options(self, options):
        print('Please make a selection.')
        for i, opt_tuple in enumerate(options):
            print('[{}] {}'.format(i, opt_tuple[0]))
        choice = int(input('> '))
        limit = self.session.SESSION_LIMIT
        if self.session.expired():
            print('Sorry, you have been idle for longer than {} seconds. Your session has expired.'.format(limit))
            return -1
        return choice

def main():
    system = StudentInformationSystem()
    system.start()

if __name__ == '__main__':
    main()