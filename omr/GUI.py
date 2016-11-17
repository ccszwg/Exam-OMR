import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QLabel, QApplication
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        uic.loadUi("resources/UI/main.ui", self)

        # make local changes
        self.logo = QPixmap("resources/OMR-logo.png")
        self.main_logo.setPixmap(self.logo)

        # Connect up the buttons
        self.button_classes.clicked.connect(self.open_classes)
        self.button_mark.clicked.connect(self.open_marking)
        self.button_create.clicked.connect(self.open_docgenerator)

        self.show()

    def open_classes(self):
        print('classes')

    def open_marking(self):
        print('mark')

    def open_docgenerator(self):
        print("docs")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
