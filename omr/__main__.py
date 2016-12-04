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
    1. Create interface for submitting papers for marking
    2. Create interface for viewing results
    3. Process results to show statistics about classes
"""
