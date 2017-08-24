import os
from assist.textprocessing import TextProcessing


class FileIter(object):
    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.tp = TextProcessing()

    def __iter__(self):
        for file_name in os.listdir(self.dir_name):
            with open(os.path.join(self.dir_name, file_name), 'r', encoding='utf-8-sig') as file:
                text = ''.join([line.strip() for line in file.readlines()])
                yield [file_name, self.tp.textprocess(text, seg=True, stop=True)]