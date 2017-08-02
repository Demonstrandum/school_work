import sys

class Ask(object):

    def __init__(self):
        print("\n== INFORMATION: ==")
        self.forename, self.surname = self.names()
        self.date = self.date()

    def dictionary(self):
        return {
            'forename': self.forename,
            'surname' : self.surname,
            'date'    : self.date
        }

    def names(self):
        return [self.asker('forename'), self.asker('surname')]

    def date(self):
        return self.asker('date')

    def asker(self, what):
        if what.lower() == 'forename' or what.lower() == 'surname': # Asks for a name, [for|sur]name
            valid = False
            name = None
            while not valid:
                name = input('Enter your {}: '.format(what))
                if name.lower() == 'quit': sys.exit()
                if ' ' in name:
                    print("\nInvalid input, there is a space in your name!\nPlese enter only one name!\n\nTry again:")
                    continue

                valid = True
            return name

        if what.lower() == 'date':
            valid = False
            date = None
            while not valid:
                date = input('Enter a {} in format DD/MM/YYYY: '.format(what))
                if date.lower() == 'quit': sys.exit()
                if not self.checkDate(date):
                    print ("\nInvalid input, your date is incorrectly formated\nor a value is out of range.\nPlease double-check the date and\n\nTry again:")
                    continue

                valid = True
            return date

        raise Exception('Could not identify type of question! This is a bug.')
        sys.exit()
        return None # Shouldn't get down here

    def checkDate(self, date):
        if len(date) > 10: return False

        dateArr = date.split('/')
        if int(dateArr[1]) > 12 or int(dateArr[1]) < 1: return False

        leap, year = False, int(dateArr[2])
        if ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0): leap = True

        daysInMonth = {
            '01': 31,
            '02': 29 if leap else 28,
            '03': 31,
            '04': 30,
            '05': 31,
            '06': 30,
            '07': 31,
            '08': 31,
            '09': 30,
            '10': 31,
            '11': 30,
            '12': 31
        }.get(dateArr[1], None)
        if daysInMonth == None: raise Exception("This is a bug! Month is of type `None`! Month not accounted for.")
        if int(dateArr[0]) > daysInMonth or int(dateArr[0]) < 1: return False # If days in mont is out of ranege
        # Perhaps incluse a year range so we dont allow years such as 9999 or 0003
        # All tests are passed:
        return True
