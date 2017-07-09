from . import generator
from . import inputParse

def id(dict):
    return generator.ID(dict).generate()

def main():
    print("")
    questions = inputParse.Ask()
    dict = questions.dictionary()
    return id(dict)

if __name__ == '__main__':
    main()
