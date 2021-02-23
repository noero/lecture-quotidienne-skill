from mycroft import MycroftSkill, intent_file_handler


class LectureQuotidienne(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('quotidienne.lecture.intent')
    def handle_quotidienne_lecture(self, message):
        self.speak_dialog('quotidienne.lecture')


def create_skill():
    return LectureQuotidienne()

