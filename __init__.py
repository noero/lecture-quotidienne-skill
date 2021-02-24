
# Add a folder named "audio" in the main directory of the skill
# and paste there all the audio files
# They should have this template name : nwt_01_Ge_F_01.mp3

from os.path import dirname, join
from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.audioservice import AudioService
from mycroft.audio import wait_while_speaking
from datetime import datetime, timedelta, date

class LectureQuotidienne(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.path = join(dirname(__file__), "audio")
        self.programme = {
            0: {0: {"name": "Genèse", "abrev": "01_Ge", "chapters": {0: "01", 1: "02", 2: "03"}}},
            1: {0: {"name": "Genèse", "abrev": "01_Ge", "chapters": {0: "04", 1: "05", 2: "06", 3: "07"}}},
            2: {0: {"name": "Genèse", "abrev": "01_Ge", "chapters": {0: "08", 1: "09", 2: "10", 3: "11"}}},
            3: {0: {"name": "Genèse", "abrev": "01_Ge", "chapters": {0: "12", 1: "13", 2: "14", 3: "15"}}}
            # TODO to continue
        }

    def initialize(self):
        self.audioservice = AudioService(self.bus)
        self.last_date = self.settings.get('last_day', (datetime.now() - timedelta(1)).strftime("%Y%m%d"))
        self.prog = self.settings.get('last_prog_count', 0)
        self.book = self.settings.get('last_book_count', 0)
        self.chapt = self.settings.get('last_chapter_count', 0)

# Définir x et y
    @intent_file_handler('reading.intent')
    def handle_quotidienne_lecture(self, message):
        if self.last_date == date.today().strftime("%Y%m%d") and self.book == len(self.programme[self.prog]) and self.chapt == len(self.programme[self.prog][self.book]["chapters"]):
            self.speak_dialog('already.done')
        else
            try:
                self.speak_dialog('reading')
                wait_while_speaking()

                if self.y == len(self.programme[self.prog][self.book]["chapters"]):
                    self.chapt = 0
                    if self.book == len(self.programme[self.prog]):
                        self.book = 0
                        self.prog = 0 if self.prog == len(self.programme) else self.prog += 1
                    else
                        self.book += 1
                else
                    self.chapt += 1

                self.playlist = []
                c = self.chapt
                b = self.book
                for j in range(b, len(self.programme[self.prog])):
                    for i in range(c, len(self.programme[self.prog][j]["chapters"])):
                        self.playlist.append(join(self.path, "nwt_" + self.programme[self.prog][j]["abrev"] + "_F_" + self.programme[self.prog][j]["chapters"][i] + ".mp3"))
                        self.chapt = i
                    c = 0
                    self.book = j
                self.audioservice.play(self.playlist)
            except Exception as e:
                self.log.error("Error: {0}".format(e))

    def stop(self):
            if self.process and self.process.poll() is None:
                self.settings["last_day"] = date.today().strftime("%Y%m%d")
                self.settings["last_prog_count"] = self.prog
                self.settings["last_book_count"] = self.book
                self.settings["last_chapter_count"] = self.chapt
                self.speak_dialog('reading.stop')
                self.process.terminate()
                self.process.wait()


def create_skill():
    return LectureQuotidienne()
