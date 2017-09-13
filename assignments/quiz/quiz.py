import sys, os
from subprocess import call

def clear(lines=100):
    fakeClear = "\n" * lines
    if 'idlelib.run' in sys.modules:
        print(fakeClear)
        return 'IDLE'
    if os.name == 'nt':
        call(['cls'])
        return 'Windows CMD/PowerShell'
    if os.name == 'posix':
        call(['clear'])
        return 'POSIX'
    print(fakeClear)
    return 'UNKNOWN'

class Quiz(object):
    def __init__(self, **kw):
        self.score = kw['score'] or 0
        self.correct = -1
        self.questions = [
            ('What is Monsieur Carrot\'s forename?', [
                [False, 'Caleb'],
                [True,  'Chris'],
                [False, 'Cameron'],
                [False, 'Clement']
            ]),
            ('What is the prefix syntax for dictionary keyword arguments in python3?', [
                [False, '*'],
                [False, '@'],
                [False, '&'],
                [True,  '**']
            ]),
            ('What is the widest object a Blue Whale can fit down it\'s throat?', [
                [True,  'Grapefruit'],
                [False, 'Car'],
                [False, 'Golf ball'],
                [False, 'Avg. American Household']
            ])
        ]

    def ask(self, question=None, to=None):
        wrong = False
        n = len(self.questions)
        if to == 'last': to = len(self.questions)
        try:
            if to < 0: to += len(self.questions) + 1
        except: pass

        if question == None or question == 'all':
            question = 1
            if to is not None:
                raise "Cannot specify `to` when `question` is not set!"
        else:
            if to is not None:
                n = to

        while question <= n:
            clear()
            self._show(question, wrong)

            chosen = input('\nChoose the correct letter: ').lower()
            if chosen == 'quit' or chosen == 'exit' or chosen == 'stop': sys.exit(0)
            if chosen == '': # <- Allow blank input
                continue

            if ord(chosen[0]) - 97 == self.correct:
                self.score += 1
                question += 1
                wrong = False
                continue

            self.score -= 1
            wrong = True

        clear()
        print("Quiz completed!\n\nYour final score is: {:d}/{:d},\n{:s}\n".format(
            self.score,
            len(self.questions),
            self._rate()
        ))

    def _rate(self):
        if self.score <= 0:
            return 'Jeesh...'
        if self.score == 1:
            return 'You can do better.'
        if self.score < 3:
            return 'That\'s Alright!'
        return 'Perfect!'

    def _show(self, n, wrong=False):
        i = n - 1
        question, answers = self.questions[i]
        wrongMsg = 'Wrong answer, try again!\n\n' if wrong else ''

        print("{:s}Question, {:d}.\t Score: {:d},\n\t\n'{:s}':".format(
            wrongMsg, n, self.score, question
        ))

        option = 97 # 97 is ASCII-8BIT for 'a' chr(97) gives 'a'
        for answer in answers:
            if answer[0]:
                self.correct = option - 97

            print("\t{:c}) {:s}".format(option, answer[1]))
            option += 1

        return self.correct


def main():
    Quiz(score=0).ask('all')
    # replace 'all' with nothing, or, ask(1, -1) which is first to last,
    # or, ask(1, 'last'), all for same effect ask(),
    # a number to ask only that question, e.g. ask(2),
    # or, two numbers for a range of questions between ...
    # ... those numbers, e.g. ask(1, 2)

if __name__ == '__main__':
    main()
