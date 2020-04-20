from validator import DatabaseReader, Validator, Privilege, Session
from users import IDAllocator, Course, Person, Student, Admin
from getpass import getpass
import sys

login_database = 'database_logins.csv'
reader = DatabaseReader()
session = None
validator = None

def prompt_options(options, session):
    print('Please make a selection.')
    for i, opt_tuple in enumerate(options):
        print('[{}] {}'.format(i, opt_tuple[0]))
    choice = int(input('> '))
    if session.expired():
        print('Sorry, you have been idle for longer than {} seconds. Your session has expired.'.format(session.SESSION_LIMIT))
        return -1
    return choice

def student_menu(session):
    '''
    Show options for a student.
    '''
    access_level = session.access_level()
    if access_level != Validator.STUDENT_ACCESS:
        print('You must be a student to access this menu.')
        return 0
    return -1

def parent_menu(session):
    '''
    Show options for a parent.
    '''
    access_level = session.access_level()
    if access_level != Validator.PARENT_ACCESS:
        print('You must be a parent to access this menu.')
        return 0
    return -1

def instructor_menu(session):
    '''
    Show options for an instructor.
    '''
    access_level = session.access_level()
    if access_level != Validator.INSTRUCTOR_ACCESS:
        print('You must be an instructor to access this menu.')
        return 0
    return -1

def admin_menu(session):
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
        ('Add an instructor', _),
    ]
    choice = prompt_options(options, session)
    return -1

def login(validator):
    email = input('Email address: ')
    pwd = getpass('Password: ')

    # Check if user exists in database
    user_rows = DatabaseReader().read(login_database)
    user_row = [row for row in user_rows if row[1] == email][0]
    user_id = int(user_row[0])
    return validator.validate(user_id)

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
    priv = login(validator)
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