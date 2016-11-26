from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from . import db_management


# todo: MOVE THIS FILE BACK TO ../interface


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        # Set up the user interface from Designer.
        uic.loadUi("interface/UI/main.ui", self)

        # add main logo to image
        self.logo = QPixmap("interface/UI/OMR-logo.png")
        self.main_logo.setPixmap(self.logo)
        self.main_logo.setScaledContents(True)

        # create all icon sizes
        self.app_icon = QtGui.QIcon()
        self.app_icon.addFile("UI/OMR-logo-icon_SMALL.png", QtCore.QSize(16, 16))
        self.app_icon.addFile("UI/OMR-logo-icon_SMALL.png", QtCore.QSize(24, 24))
        self.app_icon.addFile("UI/OMR-logo-icon_SMALL.png", QtCore.QSize(32, 32))
        self.app_icon.addFile("UI/OMR-logo-icon_SMALL.png", QtCore.QSize(48, 48))
        self.app_icon.addFile("UI/OMR-logo-icon_SMALL.png", QtCore.QSize(256, 256))
        self.setWindowIcon(self.app_icon)
        self.setWindowIcon(self.app_icon)

        # Connect up the buttons
        self.button_classes.clicked.connect(self.open_classes)
        self.button_mark.clicked.connect(self.open_marking)
        self.button_create.clicked.connect(self.open_docgenerator)

        self.w = []

    def open_classes(self):
        self.w.append(ClassWindow(self))
        self.w[-1].show()

    def open_marking(self):
        print('mark')

    def open_docgenerator(self):
        print("docs")


class ClassWindow(QMainWindow):
    def __init__(self, parent=MainWindow):
        super().__init__()

        # Set up the user interface from Designer.
        uic.loadUi("interface/UI/classes.ui", self)
        self.text_add_widget.setHidden(True)

        # initialise tables
        self.Classes = db_management.Table("Classes")
        self.Students = db_management.Table("Students")

        # build additional parts of interface
        self.create_combobox()
        self.comboBox_classes.setCurrentIndex(-1)

        # connect buttons
        self.button_createclass.clicked.connect(self.open_createclass)
        self.button_savetext.clicked.connect(self.save_text)
        self.button_loadclass.clicked.connect(self.initialise_table)
        self.button_addstudent.clicked.connect(self.open_addstudent)

        # initialise variables
        self.add_mode = None

    def open_createclass(self):
        self.add_mode = "class"
        self.text_add_widget.setHidden(False)
        self.text_add.setText("Enter Class Name")

    def open_addstudent(self):
        self.add_mode = "student"
        self.text_add_widget.setHidden(False)
        self.text_add.setText("Enter student name")

    def toggle_textwidget(self):
        self.text_add_widget.setHidden(not self.text_add_widget.isHidden())

    def save_text(self):
        # todo: add user error message for if name already exists

        if self.add_mode == "class":
            if not self.Classes.name_exists(self.text_add.text()):
                self.Classes.add([self.text_add.text()])
                self.create_combobox(selected="last")
            self.toggle_textwidget()

        elif self.add_mode == "student":
            class_ID = str(self.Classes.get_ID(' WHERE Class_Name="' +
                                               str(self.comboBox_classes.currentText()) + '"')[0][0])
            if not self.Students.name_exists(self.text_add.text(), " AND class_ID=" + class_ID):
                student_name = self.text_add.text()

                self.Students.add([student_name, class_ID])

                self.open_addstudent()
                self.initialise_table()

    def create_combobox(self, selected=None):

        names = self.Classes.get_names()

        self.comboBox_classes.clear()

        for i in names:
            self.comboBox_classes.addItem(i[0])

        if selected == "last":
            self.comboBox_classes.setCurrentIndex(len(names) - 1)
            self.initialise_table()

    def initialise_table(self):

        self.table_students.setRowCount(0)

        class_name = str(self.comboBox_classes.currentText())

        class_ID = self.Classes.get_ID(' WHERE Class_Name="' + class_name + '"')

        names = self.Students.get_names(' WHERE Class_ID="' + str(class_ID[0][0]) + '"')

        for i in names:
            rowPosition = self.table_students.rowCount()
            self.table_students.insertRow(rowPosition)
            self.table_students.setItem(rowPosition, 0, QTableWidgetItem(str(i[0])))
