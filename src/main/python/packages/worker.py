import os, csv, time

from PySide2 import QtCore

from packages.api.note import Note

class Worker(QtCore.QObject):

    finished = QtCore.Signal()
    step = QtCore.Signal(object)

    def __init__(self, file):
        super().__init__()
        self.file = file

    def import_csv(self):
        if self.file:
            with open(self.file, newline='') as f:
                for row in csv.reader(f):
                    if row:
                        note = Note(title=row[0], account=row[1], password=row[2], content=row[3])
                        note.save()
                        self.step.emit(note)
                        time.sleep(0.01)
            self.finished.emit()