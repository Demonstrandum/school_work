from . import generator
from . import inputParse

def id():
    questions = inputParse.Ask()
    dict = questions.dictionary()
    return generator.ID(dict).generate()

def main():
    print(id())

if __name__ == '__main__':
    main()
