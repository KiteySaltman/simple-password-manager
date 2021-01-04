import os
import json
from uuid import uuid4
from glob import glob

from packages.api.constants import NOTES_DIR


def get_notes():
    notes = []
    files = glob(os.path.join(NOTES_DIR, "*.json"))
    for file in files:
        with open(file, "r") as f:
            note_data = json.load(f)
            note_uuid = os.path.splitext(os.path.basename(file))[0]

            note_title = note_data.get("title")
            note_account = note_data.get("account")
            note_password = note_data.get("password")
            note_content = note_data.get("content")

            note = Note(uuid=note_uuid, title=note_title,
                        account=note_account, password=note_password,
                        content=note_content)
            notes.append(note)
    return notes


class Note:
    def __init__(self, title="", account="", password="", content="", uuid=None):
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = str(uuid4())

        self.title = title
        self.content = content
        self.account = account
        self.password = password

    def __repr__(self):
        return f"{self.title} {self.account} {self.password} ({self.uuid})"

    def __str__(self):
        return repr(self)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if isinstance(value, str):
            self._content = value
        else:
            raise TypeError("Valeur invalide, chaine de caractères uniquement.")

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, value):
        if isinstance(value, str):
            self._account = value
        else:
            raise TypeError("Valeur invalide, chaine de caractères uniquement.")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if isinstance(value, str):
            self._password = value
        else:
            raise TypeError("Valeur invalide, chaine de caractères uniquement.")

    def delete(self):
        os.remove(self.path)
        if os.path.exists(self.path):
            return False
        return True

    @property
    def path(self):
        return os.path.join(NOTES_DIR, f"{self.uuid}.json")

    def save(self):
        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)

        data = {"title": self.title,
                "content": self.content,
                "password": self.password,
                "account": self.account}

        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)
