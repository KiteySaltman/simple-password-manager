import os
import csv

from packages.api.note import get_notes, Note


def import_csv(file=""):
    if file:
        with open(file, newline='') as f:
            for row in csv.reader(f):
                if row and row[0] != "Title" and row[1] != "Account" and \
                        row[2] != "Password" and row[3] != "Other information":
                    note = Note(title=row[0], account=row[1], password=row[2], content=row[3])
                    note.save()
        return True
