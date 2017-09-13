import sys
import copy

def fakeClear(lines=100):
    print("\n" * lines)

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

    def ask(self, question=None):
        wrong = False
        n = len(self.questions)
        if question == None or question.lower() == 'all':
            question = 1
        else:
            n = question

        while question <= n:
            fakeClear()
            self._show(question, wrong)

            chosen = input('\nChoose the correct letter: ').lower()
            if chosen == 'quit' or chosen == 'exit' or chosen == 'stop': sys.exit(0)
            if chosen == '':    # <- Blank input
                chosen += ' '   # <- Just non-empty
                self.score += 1 # <- Compensate for blank answer

            if ord(chosen[0]) - 97 == self.correct:
                self.score += 1
                question += 1
                wrong = False
                continue

            self.score -= 1
            wrong = True

        fakeClear()
        print("Quiz completed!\n\nYour final score is: {:d}!\n{:s}\n".format(
            self.score,
            self.rate()
        ))

    def rate(self):
        if self.score < 0:
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

if __name__ == '__main__':
    main()
