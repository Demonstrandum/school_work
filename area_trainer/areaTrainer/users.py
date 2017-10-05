"""Adding a checking users"""

import re  # Regular Expression support
import json
from time import gmtime, strftime

DATABASE = [{}]
EXAMPLE_DATABASE = [
    {
        'username': 'sam',
        'password': 'Hello123',
        'sessions': [
            ['2017-09-25 12:50:20', '2017-09-25 12:50:20'],
            ['2017-09-29 14:00:21', '2017-09-29 15:25:50']
        ],
        'shapes':   [['triangle', 6], ['square', 2]]
    },
    {
        'username': 'tom',
        'password': 'dorW009',
        'sessions': [
            ['2013-10-02 23:00:10', '2013-10-02 23:00:10'],
            ['2014-11-01 14:00:21', '2014-11-02 01:25:50']
        ],
        'shapes':   [['triangle', 8], ['square', 1]]
    }
]


class Users(object):
    """Abstract class for Login & Register"""
    def __init__(self, database=None):
        self.database = database
        if database is None:
            self.database = DATABASE

    def save(self, file_name='logins.json'):
        """Save to database file"""
        json_dump = json.dumps(self.database)
        with open(file_name, 'w') as file:
            file.write(json_dump)

        return self.database

    def load(self, file_name='logins.json'):
        """Load database file to self.database"""
        json_string = ''
        with open(file_name, 'r') as file:
            json_string = file.read()
            self.database = json.loads(json_string)

        if len(self.database[0]) < 1:
            self.database.pop(0)

        return self.database


class Login(Users):
    """Add a user to dict database"""
    def __init__(self, username, password, database):
        super().__init__(database)
        self.username = username
        self.password = password
        self.database = database
        self.logged_in = False

    def exists(self):
        """Checks username"""
        try:
            return self.username in [users['username'] for users in self.database]
        except KeyError:
            return False

    def login(self):
        """Checks username and password"""
        try:
            for user in self.database:
                if (user['username'] == self.username and
                        user['password'] == self.password):
                    self.logged_in = True
                    break
        except KeyError:
            return False

        return self.logged_in


class Register(Users):
    """Register users and add them to your database"""
    def __init__(self, user, passwd, data):
        super().__init__(data)
        self.database = data
        self.username = user
        self.password = passwd

    def add(self):
        """Add method mutates login database"""
        user_info = {
            'username': self.username,
            'password': self.password,
            'sessions': [
                [
                    strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                    strftime("%Y-%m-%d %H:%M:%S", gmtime())
                ]
            ],
            'shapes': []
        }
        self.database.append(user_info)
        return self.database

    def taken(self):
        """Check if the username is taken"""
        try:
            return self.username in [users['username'] for users in self.database]
        except KeyError:
            return False

    def validate(self, name_length=40, password_length=8):
        """Check if username/password are valid"""
        message = {
            'valid': False,
            'error': None
        }

        if self.taken():
            message['error'] = "Username taken!"
            return message

        if re.match('.*[^A-Za-z0-9\-_\s].*', self.username):
            message['error'] = "Username must be\nalphanumeric\n('-' and '_' allowed)"
            return message

        if len(self.username) > name_length:
            message['error'] = "Username too long!\n({:d} max length)".format(name_length)
            return message

        if len(self.password) < password_length:
            message['error'] = "Passwrod must be\nat least 8 characters"
            return message

        if (self.password.upper() == self.password or
                self.password.lower() == self.password):
            message['error'] = "Password must have\nupper and lower\ncase letters!"
            return message

        if not any(char.isdigit() for char in self.password):
            message['error'] = "Password must\ncontain number(s)!"
            return message

        if not re.match('.*[^A-Za-z0-9].*', self.password):
            message['error'] = "Must contain\nspecial character(s)!"
            return message

        if re.match('.*\s.*', self.password):
            message['error'] = "Must can't\nhave space(s)!"
            return message

        # Otherwise, were happy
        message['valid'] = True
        message['error'] = 'Success'
        return message
