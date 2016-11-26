from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QDialog

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

        # connect buttons
        self.button_createclass.clicked.connect(self.open_createclass)
        self.button_savetext.clicked.connect(self.save_text)

        # initialise variables
        self.add_mode = None

    def open_createclass(self):
        self.add_mode = "class"
        self.text_add_widget.setHidden(False)
        self.text_add.setText("Enter Class Name")

    def toggle_textwidget(self):
        self.text_add_widget.setHidden(not self.leftWidget.isHidden())

    def save_text(self):
        if self.add_mode == "class":
            print("1")
            if not self.Classes.name_exists(self.text_add.text()):
                print("2")
                self.Classes.add(self.text_add.text())


class NewClassWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        # Set up the user interface from Designer.
        uic.loadUi("interface/UI/newclass.ui", self)

        # initialise database access
        Class = db_management.Table("Classes")

        # connect buttons
