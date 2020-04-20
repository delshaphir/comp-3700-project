from validator import DatabaseReader, Validator, Privilege, Session
from users import IDAllocator, Course, Person, Student, Admin
from getpass import getpass
import sys

reader = DatabaseReader()
session = None
validator = None

def prompt_options(options):
    print('Please make a selection.')
    for i, opt_tuple in enumerate(options):
        print('[{}] {}'.format(i, opt_tuple[0]))
    return int(input('> '))

def student_menu(access_level):
    '''
    Show options for a student.
    '''
    if access_level != Validator.STUDENT_ACCESS:
        print('You must be a student to access this menu.')
        return 0
    return -1

def parent_menu(access_level):
    '''
    Show options for a parent.
    '''
    if access_level != Validator.PARENT_ACCESS:
        print('You must be a parent to access this menu.')
        return 0
    return -1

def instructor_menu(access_level):
    '''
    Show options for an instructor.
    '''
    if access_level != Validator.INSTRUCTOR_ACCESS:
        print('You must be an instructor to access this menu.')
        return 0
    return -1

def admin_menu(access_level):
    '''
    Show options for an administrator.
    '''
    if access_level != Validator.ADMIN_ACCESS:
        print('You must be an administrator to access this menu.')
        return 0
    print('Welcome to the Administrator menu.')
    options = [
        ('Create a course', student_menu),
        ('Assign a course to an instructor', parent_menu),
        ('Add an instructor', _),
    ]
    choice = prompt_options(options)
    return -1

def login(validator):
    email = input('Email address: ')
    pwd = getpass('Password: ')

    # Check if user exists in database
    user_rows = DatabaseReader().read('database.csv')
    user_row = [row for row in user_rows if row[1] == email][0]
    user_id = int(user_row[0])
    return validator.validate(user_id)

def menu(session: Session):
    options = [
        ('Access Student controls', student_menu),
        ('Access Parent controls', parent_menu),
        ('Access Instructor controls', instructor_menu),
        ('Access Administrator controls', admin_menu),
        ('Exit', None)
    ]
    choice = prompt_options(options)
    ret = options[choice][1](session.access_level())
    if ret == 0:
        menu(session)

def main():
    # Initialize validator
    validator = Validator('database.csv')
    
    print('Welcome to the Student Information System.')
    priv = login(validator)
    if priv is None:
        print('Invalid user.')
        sys.exit()

    # Initialize session
    session = Session(priv)

    # Show menu()
    menu(session)

if __name__ == '__main__':
    main()