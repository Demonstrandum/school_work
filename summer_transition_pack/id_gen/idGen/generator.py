class ID(object):
    def __init__(self, dict):
        self.forename = dict['forename'].upper()
        self.surname  = dict['surname'].upper()
        self.date     = dict['date']

    def generate(self):
        date = self.date.split('/')
        return (
            date[-1] + date[-2] + date[-3]
            + self.surname + self.forename[0]
            + str(len(self.forename))
        )
