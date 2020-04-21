from student_system.users import IDAllocator, Course
from student_system.validator import DatabaseReader, Validator, Privilege, Session
from getpass import getpass
from typing import List
import sys

login_database = 'database_logins.csv'
student_database = 'database_students.csv'
reader = DatabaseReader()
session = None
validator = None

def prompt_options(options: List[tuple], session: Session):
    print('Please make a selection.')
    for i, opt_tuple in enumerate(options):
        print('[{}] {}'.format(i, opt_tuple[0]))
    choice = int(input('> '))
    if session.expired():
        print('Sorry, you have been idle for longer than {} seconds. Your session has expired.'.format(session.SESSION_LIMIT))
        return -1
    return choice

def student_menu(session: Session):
    '''
    Show options for a student.
    '''
    access_level = session.access_level()
    if access_level != Validator.STUDENT_ACCESS:
        print('You must be a student to access this menu.')
        return 0
    return -1

def parent_menu(session: Session):
    '''
    Show options for a parent.
    '''
    access_level = session.access_level()
    if access_level != Validator.PARENT_ACCESS:
        print('You must be a parent to access this menu.')
        return 0
    return -1

def instructor_menu(session: Session):
    '''
    Show options for an instructor.
    '''
    access_level = session.access_level()
    if access_level != Validator.INSTRUCTOR_ACCESS:
        print('You must be an instructor to access this menu.')
        return 0
    return -1

def admin_menu(session: Session):
    '''
    Show options for an administrator.
    '''
    access_level = session.access_level()
    if access_level != Validator.ADMIN_ACCESS:
        print('You must be an administrator to access this menu.')
        return 0
    print('Welcome to the Administrator menu.')
    options = [
        ('Create a course', student_menu),
        ('Assign a course to an instructor', parent_menu),
    ]
    choice = prompt_options(options, session)
    return -1

def login(validator: Validator):
    email = input('Email address: ')
    pwd = getpass('Password: ')

    # Check if user exists in database
    return validator.validate(email)

def menu(session: Session):
    options = [
        ('Access Student controls', student_menu),
        ('Access Parent controls', parent_menu),
        ('Access Instructor controls', instructor_menu),
        ('Access Administrator controls', admin_menu),
        ('Exit', lambda _: -1)
    ]
    choice = prompt_options(options, session)
    ret = options[choice][1](session)
    if ret == 0:
        menu(session)
    else:
        return

def main():
    # Initialize validator
    validator = Validator(login_database)
    
    print('Welcome to the Student Information System.')
    user_id, priv = login(validator)
    if priv is None:
        print('Invalid user.')
        sys.exit()

    # Initialize session
    session = Session(priv)

    # Show menu()
    menu(session)

    print('You have been logged out of the Student Information System.')

if __name__ == '__main__':
    main()