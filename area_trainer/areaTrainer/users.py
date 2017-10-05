"""Adding a checking users"""

import json
from time import gmtime, strftime


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
            self.database = EXAMPLE_DATABASE

    def save(self, file='logins.json'):
        """Save to database file"""
        json_dump = json.dumps(self.database)
        with open(file, 'w') as file:
            file.write(json_dump)

        return self.database

    def load(self, file='logins.json'):
        """Load database file to self.database"""
        json_string = ''
        with open(file, 'r') as file:
            json_string = file.read()
            self.database = json.loads(json_string)

        return self.database


class Login(Users):
    """Add a user to dict database"""
    def __init__(self, user, password, database):
        super().__init__(database)
        self.username = user
        self.password = password
        self.database = database
        self.logged_in = False

    def exists(self):
        """Checks username"""
        return self.username in [users['username'] for users in self.database]

    def login(self):
        """Checks username and password"""
        for user in self.database:
            if (user['username'] == self.username and
                    user['password'] == self.password):
                self.logged_in = True
                break

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
        return self.username in [users['username'] for users in self.database]
