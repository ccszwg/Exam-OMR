import sys

from PyQt5.QtWidgets import QApplication
from controllers.GUI import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())

"""
    todo:
    1. Draw bar chart showing data
"""
