import json


class LanguageInterface(object):
    def __init__(self):
        infile = open("language.json", "r")
        self.language = json.load(infile)
        infile.close()

    def find_context(self, word):
        parent_cat = "No matching categories"
        for category in self.language["basics"]:
            for value in category["values"]:
                if word.lower() == value:
                    parent_cat = category["type"]
                    break
        return parent_cat

    # def context_response(self, category):


def main():
    test = LanguageInterface()
    while True:
        word = raw_input("Try a word: ")
        out = test.find_word(word)
        print out

if __name__ == '__main__':
    main()
