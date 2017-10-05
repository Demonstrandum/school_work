"""Client for Area Trainers"""

import getpass
import os
import tkinter as tk

import areaTrainer as at


def login(database, file):
    """Login and check to AT"""
    exists = False
    while not exists:
        name = input('Enter your username: ')
        passwd = getpass.getpass('Enter password: ')
        log = at.Login(name, passwd, database)
        exists = log.login()
        if not exists:
            print('Username or password is invalid!')

    log.save(file)
    return [name, passwd]


def register(database, file):
    """Register to AT"""
    taken = True
    while taken:
        username = input('Enter a username: ')
        if at.Login(username, '', database).exists():
            print('This username is taken!')
            continue
        taken = False

    match = False
    while not match:
        valid = False
        while not valid:
            password = getpass.getpass('Enter a password: ')
            if len(password) < 6:
                print('Password must be more than 6 characters long!')
                continue
            if password.upper() == password or \
               password.lower() == password:
                print('''
The password must
contain at least one upper or
lower case character!''')
                continue
            if not any(char.isdigit() for char in password):
                print('Must contain at least one number!')
                continue
            valid = True

        reenter = getpass.getpass('Re-enter password: ')
        if not reenter == password:
            print('Your passwords do not match, try again!')
            continue

        match = True

    reg_obj = at.Register(
        username,
        password,
        database
    )
    reg_obj.add()
    reg_obj.save(file)
    return [username, password]


file = "{}/logins.json".format(os.getcwd())
# Make file if it does not exist
if not os.path.exists(file):
    at.Users().save(file)


root = tk.Tk()
root.title("Register or Login")
root.configure(background='white')

name_label = tk.Label(root, text="Username", background='white')
name_label.pack(side=tk.LEFT)
name_entry = tk.Entry(root, bd=5, background='white')
name_entry.pack(side=tk.RIGHT)

pass_label = tk.Label(root, text="Username", background='white')
pass_label.pack(side=tk.LEFT)
pass_entry = tk.Entry(root, bd=5, background='white')
pass_entry.pack(side=tk.RIGHT)

root.mainloop()

# logins = at.Users().load()
# username = password = None

# logged_in = False
# while not logged_in:
#     print('Would you like to login, or register [L/r]')
#     option = input('> ')

#     if not option.lower() == 'r':
#         logger = login(logins, file)
#         username, password = logger
#         if logger:
#             break
#     else:
#         reg = register(logins, file)
#         username, password = reg
#         if reg:
#             break
# print('Succsess.')
# print('Logged in as {}'.format(username))

# Verbose extra database output
print('Users saved, user database: ')
print(at.Users().load())
