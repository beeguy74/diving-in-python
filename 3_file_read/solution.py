import os

class FileReader():
    def __init__(self, name):
        self.name = name

    def read(self):
        try:
            with open(self.name) as f:
                    return f.read()
        except:
            return ""
        