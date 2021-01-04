import os

from packages.api.note import get_notes


def export_to_csv(file=""):
    if file:
        file_path, file_type = os.path.splitext(file)

        if file_type != ".csv":
            file_type = ".csv"

        notes = get_notes()
        file = file_path + file_type
    else:
        file = "export.csv"

    with open(file, "w") as f:
        f.write("title,account,password,other_information\n")
        for note in notes:
            f.write(f"{note.title},{note.account},{note.password},{note.content}\n")
