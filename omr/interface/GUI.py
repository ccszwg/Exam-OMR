import sys

from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        # Set up the user interface from Designer.
        uic.loadUi("UI/main.ui", self)

        # add main logo to image
        self.logo = QPixmap("UI/OMR-logo.png")
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

        # Create other windows
        self.classes = ClassWindow(self)

    def open_classes(self):
        self.classes.show()


    def open_marking(self):
        print('mark')

    def open_docgenerator(self):
        print("docs")


class ClassWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        # Set up the user interface from Designer.
        uic.loadUi("UI/classes.ui", self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
