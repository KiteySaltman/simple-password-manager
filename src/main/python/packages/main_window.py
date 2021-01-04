import os
from functools import partial

from PySide2 import QtWidgets, QtGui, QtCore

from password_generator import PasswordGenerator

from packages.api.note import Note, get_notes
from packages.api.export import export_to_csv
from packages.api.import_csv import import_csv

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("Password Manager")
        self.setup_ui()
        self.populate_note()


    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.add_widget_to_layouts()
        self.add_actions_to_toolbar()
        self.modify_widgets()
        self.setup_connections()


    def create_widgets(self):
        self.toolbar = QtWidgets.QToolBar()
        self.lw_notes = QtWidgets.QListWidget()

        self.lbl_search = QtWidgets.QLabel("Search :")
        self.le_search = QtWidgets.QLineEdit()

        self.lbl_content = QtWidgets.QLabel("Other information :")
        self.te_content = QtWidgets.QTextEdit()

        self.lbl_account = QtWidgets.QLabel("Account name:")
        self.le_account = QtWidgets.QLineEdit()

        self.lbl_password = QtWidgets.QLabel("Password :")
        self.le_password = QtWidgets.QLineEdit()

        self.btn_cpy_pswd = QtWidgets.QPushButton()

        self.btn_save = QtWidgets.QPushButton("Save (Ctrl+S)")

        self.delete_message = QtWidgets.QMessageBox()

        self.main_widget = QtWidgets.QTabWidget()


    def modify_widgets(self):
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

        self.btn_save.setCursor(QtCore.Qt.PointingHandCursor)

        self.delete_message.setStyleSheet("width:100px;")
        self.delete_message.setText("This account will be delete.")
        self.delete_message.setInformativeText("Are you sure want to continue?")
        self.delete_message.setStandardButtons( QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel )
        self.delete_message.setDefaultButton(QtWidgets.QMessageBox.Cancel)

        # DISPLAY *** INSTEAD OF DEFAULT STRING
        self.le_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.PasswordEchoOnEdit)

        # CHANGE BUTTON COPY TO CLIPBOARD
        icon = self.ctx.get_resource('clipboard.svg')
        self.btn_cpy_pswd.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_cpy_pswd.setIcon(QtGui.QIcon(icon))
        self.btn_cpy_pswd.setIconSize(QtCore.QSize(38,38))
        self.btn_cpy_pswd.setStyleSheet("background-color: transparent;")
        self.btn_cpy_pswd.setToolTip("Copy to clipboard")


    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self.main_widget)


    def add_widget_to_layouts(self):
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.setCentralWidget(self.main_widget)

        self.main_layout.addWidget(self.lbl_search, 0, 0, 1, 2)
        self.main_layout.addWidget(self.le_search, 1, 0, 1, 2)

        self.main_layout.addWidget(self.lw_notes, 2, 0, 8 ,1)

        self.main_layout.addWidget(self.lbl_account, 3, 1, 1, 1)
        self.main_layout.addWidget(self.le_account, 4, 1, 1, 1)

        self.main_layout.addWidget(self.lbl_password, 5, 1, 1, 1)
        self.main_layout.addWidget(self.le_password, 6, 1, 1, 1)
        self.main_layout.addWidget(self.btn_cpy_pswd, 6, 2, 1, 1)

        self.main_layout.addWidget(self.lbl_content, 7, 1, 1, 1)
        self.main_layout.addWidget(self.te_content, 8, 1, 1, 1)

        self.main_layout.addWidget(self.btn_save, 9, 1, 1, 1)


    def setup_connections(self):
        self.lw_notes.itemSelectionChanged.connect(self.populate_note_content)
        self.btn_save.clicked.connect(self.save_note)
        self.btn_cpy_pswd.clicked.connect(self.copy_to_clipboard)
        self.le_search.textChanged.connect(self.search)

        # ADD SHORTCUT
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+A"), self.lw_notes, self.create_note)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+P"), self.lw_notes, self.random_password)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self.lw_notes, self.save_note)
        QtWidgets.QShortcut(QtGui.QKeySequence("Backspace"), self.lw_notes, self.delete_selected_note)
        QtWidgets.QShortcut(QtGui.QKeySequence("Delete"), self.lw_notes, self.delete_selected_note)
    #END SETUP UI


    def add_actions_to_toolbar(self):

        icons = ["create_note","random_password","delete_selected_note", "import_csv", "export"]

        for icon in icons:
            icon_ = self.ctx.get_resource(icon + '.svg')
            action = self.toolbar.addAction(QtGui.QIcon(icon_), icon.replace("_", " "))
            eval(f"action.triggered.connect(partial(self.{icon}))")


    def add_note_to_listwidget(self, note):
        lw_item = QtWidgets.QListWidgetItem(note.title)
        lw_item.note = note
        self.lw_notes.addItem(lw_item)


    def copy_to_clipboard(self):
        selected_item = self.get_selected_lw_item()
        if selected_item:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(self.le_password.text())


    def create_note(self):
        title, result = QtWidgets.QInputDialog.getText(self, "Add", "Title app / Website: ")
        if result and title:
            note = Note(title=title.capitalize())
            note.save()
            self.add_note_to_listwidget(note)
            self.lw_notes.sortItems(QtCore.Qt.AscendingOrder)


    def export(self):
        file, type = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', filter="csv")
        if file:
            export_to_csv(file=file)


    def delete_selected_note(self):
        selected_item = self.get_selected_lw_item()
        if selected_item:
            response = self.delete_message.exec_()
            if response == QtWidgets.QMessageBox.Yes:
                result = selected_item.note.delete()
                if result:
                    self.lw_notes.takeItem( self.lw_notes.row(selected_item) )


    def get_selected_lw_item(self):
        selected_items = self.lw_notes.selectedItems()
        if selected_items:
            return selected_items[0]
        return None


    def import_csv(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Import CSV file')
        if file:
            file_path, file_type = os.path.splitext(file[0])
            if file_type == ".csv":
                result = import_csv(file=file[0])
                if result:
                    self.lw_notes.clear()
                    self.populate_note()
            else:
                print("not csv file")


    def populate_note(self):
        notes = get_notes()
        for note in notes:
            self.add_note_to_listwidget(note)
        self.lw_notes.sortItems(QtCore.Qt.AscendingOrder)


    def populate_note_content(self):
        selected_item = self.get_selected_lw_item()
        if selected_item:
            self.te_content.setText(selected_item.note.content)
            self.le_password.setText(selected_item.note.password)
            self.le_account.setText(selected_item.note.account)
        else:
            self.te_content.clear()
            self.le_password.clear()
            self.le_account.clear()


    def save_note(self):
        selected_item = self.get_selected_lw_item()
        if selected_item:
            selected_item.note.content = self.te_content.toPlainText()
            selected_item.note.account = self.le_account.text()
            selected_item.note.password = self.le_password.text()
            selected_item.note.save()


    def search(self, value):
        if len(value) <= 0:
            self.lw_notes.clear()
            self.populate_note()
        else:
            self.lw_notes.clear()
            notes = get_notes()
            for note in notes:
                title = note.title.lower()
                if (title.find( value.lower() ) != -1):
                    self.add_note_to_listwidget(note)


    def random_password(self):
        selected_item = self.get_selected_lw_item()
        if selected_item:
            pwo = PasswordGenerator()
            pwo.minlen = 8  # (Optional)
            pwo.maxlen = 16  # (Optional)
            pwo = pwo.generate()
            self.le_password.setText(pwo)