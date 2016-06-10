import json


class LanguageInterface(object):
    def __init__(self):
        infile = open("language.json", "r")
        self.language = json.load(infile)
        infile.close()

    def get_context(self, phrase):
        topic = self.get_topic(phrase)
        subject = self.get_subject(topic, phrase)
        activity = self.get_activity(topic, phrase)
        return "Topic: " + topic + " Subject: " + subject + " Activity: " + activity

    def get_topic(self, phrase):
        parent_topic = "none"
        for topic in self.language["topics"]:
            for keyword in topic["keywords"]:
                if keyword in phrase.lower():
                    parent_topic = topic["topic"]
                    break
        return parent_topic

    def get_subject(self, topic, phrase):
        child_subject = "none"
        for top in self.language["topics"]:
            if top["topic"] == topic:
                for subject in top["subjects"]:
                    if subject in phrase.lower():
                        child_subject = subject
                        break
        return child_subject

    def get_activity(self, topic, phrase):
        child_activity = "none"
        for top in self.language["topics"]:
            if top["topic"] == topic:
                if len(top["activities"]) > 1:
                    for activity in top["activities"]:
                        if activity in phrase.lower():
                            child_activity = activity
                            break
                else:
                    child_activity = top["activities"][0]
        return child_activity

    # def context_response(self, category):


def main():
    test = LanguageInterface()
    while True:
        phrase = raw_input("Try a phrase: ")
        out = test.get_context(phrase)
        print out

if __name__ == '__main__':
    main()
