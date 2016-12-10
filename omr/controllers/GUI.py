import os

from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QFileDialog

from . import db_management
from . import doc_generator
from . import improcessing


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
        self.w.append(MarkWindow(self))
        self.w[-1].show()

    def open_docgenerator(self):
        self.w.append(AnswerSheet_Generator(self))
        self.w[-1].show()


class ClassWindow(QMainWindow):
    # todo: let user press enter instead of button in textboxes
    def __init__(self, parent=MainWindow):
        super().__init__()

        self.w = []

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
        self.button_addstudent.clicked.connect(self.open_addstudent)
        self.button_deleteclass.clicked.connect(self.delete_class)
        self.table_students.cellClicked.connect(self.cell_clicked)
        self.button_deletestudent.clicked.connect(self.delete_student)
        self.comboBox_classes.currentIndexChanged.connect(self.initialise_table)
        self.button_close.clicked.connect(self.close)

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

    def delete_class(self):
        self.w.append(Dialog("confirm", "Confirm", "Are you sure you want to delete this class?"))
        self.w[-1].show()

        if self.w[-1].exec_():
            class_name = str(self.comboBox_classes.currentText())
            class_ID = self.Classes.get_ID(' WHERE Class_Name="' + class_name + '"')

            self.Classes.delete(' WHERE Class_ID=' + str(class_ID[0][0]))

            self.comboBox_classes.removeItem(self.comboBox_classes.findText(class_name))

    def toggle_textwidget(self):
        self.text_add_widget.setHidden(not self.text_add_widget.isHidden())

    def save_text(self):
        # todo: add user error message for if name already exists

        if self.add_mode == "class":
            if not self.Classes.name_exists(self.text_add.text()):
                self.Classes.add([self.text_add.text()])
                self.comboBox_classes.addItem(self.text_add.text())
                self.comboBox_classes.setCurrentIndex(self.comboBox_classes.count() - 1)
                self.initialise_table()

            self.toggle_textwidget()

        elif self.add_mode == "student":
            class_ID = str(self.Classes.get_ID(' WHERE Class_Name="' +
                                               str(self.comboBox_classes.currentText()) + '"')[0][0])
            if not self.Students.name_exists(self.text_add.text(), " AND class_ID=" + class_ID):
                student_name = self.text_add.text()

                self.Students.add([student_name, class_ID])

                self.open_addstudent()
                self.initialise_table()

    def create_combobox(self, selected=""):

        names = self.Classes.get_names()

        self.comboBox_classes.clear()

        for i in names:
            self.comboBox_classes.addItem(i[0])

    def cell_clicked(self, row, column):
        self.button_deletestudent.setEnabled(True)

    def delete_student(self):
        class_name = str(self.comboBox_classes.currentText())
        class_ID = self.Classes.get_ID(' WHERE Class_Name="' + class_name + '"')

        name = self.table_students.currentItem().text()
        self.Students.delete(' WHERE Student_Name="' + name + '" AND Class_ID=' + str(class_ID[0][0]))

        self.initialise_table()

    def initialise_table(self):

        self.button_addstudent.setEnabled(True)
        self.button_deleteclass.setEnabled(True)

        self.table_students.setRowCount(0)

        class_name = str(self.comboBox_classes.currentText())

        class_ID = self.Classes.get_ID(' WHERE Class_Name="' + class_name + '"')

        names = self.Students.get_names(' WHERE Class_ID="' + str(class_ID[0][0]) + '"')

        for i in names:
            rowPosition = self.table_students.rowCount()
            self.table_students.insertRow(rowPosition)
            self.table_students.setItem(rowPosition, 0, QTableWidgetItem(str(i[0])))


class AnswerSheet_Generator(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        # Set up the user interface from Designer.
        uic.loadUi("interface/UI/answersheet_generator.ui", self)

        self.Classes = db_management.Table("Classes")
        self.Students = db_management.Table("Students")
        self.Tests = db_management.Table("Tests")

        self.create_combobox()
        self.comboBox_classes.setCurrentIndex(-1)

        # connect buttons
        self.slider_questions.valueChanged.connect(self.sliderquestion_values)
        self.slider_numoptions.valueChanged.connect(self.slideroption_values)
        self.button_save.clicked.connect(self.save_dialog)
        self.comboBox_classes.currentIndexChanged.connect(self.check_options_valid)
        self.button_generate.clicked.connect(self.generate_questions)

        self.fileloc = None

    def sliderquestion_values(self):
        self.label_numquestions.setText(str(self.slider_questions.value()))

    def slideroption_values(self):
        self.label_numoptions.setText(str(self.slider_numoptions.value()))

    def create_combobox(self, selected=""):
        names = self.Classes.get_names()

        self.comboBox_classes.clear()

        for i in names:
            self.comboBox_classes.addItem(i[0])

    def save_dialog(self):
        # todo: change this to save one file
        self.fileloc = QFileDialog.getExistingDirectory(self, 'Select folder to save to')
        self.label_savelocation.setText(self.fileloc)

        self.check_options_valid()

    def check_options_valid(self):
        if self.fileloc is not None and self.comboBox_classes.currentText() is not "":
            self.button_generate.setEnabled(True)

    def generate_questions(self):
        # create test record
        self.Tests.add([self.textbox_testname.text(), self.slider_questions.value()])

        class_ID = str(self.Classes.get_ID(' WHERE Class_Name="' + str(self.comboBox_classes.currentText())
                                           + '"')[0][0])
        names = [i[0] for i in self.Students.get_names(' WHERE Class_ID=' + class_ID)]
        student_info = []

        for i in names:
            ID = str(self.Students.get_ID(' WHERE Class_ID=' + class_ID + ' AND Student_Name="' + i + '"')[0][0])
            student_info.append({"Name": i, "ID": ID})

        doc_generator.generate(student_info, self.slider_questions.value(),
                               self.slider_numoptions.value(), self.fileloc)

        # todo: create loading bar


class MarkWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.Results = db_management.Table("Results")

        # Set up the user interface from Designer.
        uic.loadUi("interface/UI/mark.ui", self)
        self.progressBar.setHidden(True)

        # connect buttons
        self.button_selectfolder.clicked.connect(self.open_dialog)
        self.button_markpapers.clicked.connect(self.mark_papers)

        self.w = []

    def open_dialog(self):
        self.fileloc = QFileDialog.getExistingDirectory(self, 'Select folder containing answer papers')
        self.label_folderlocation.setText(self.fileloc)
        self.button_markpapers.setEnabled(True)

    def mark_papers(self):
        self.progressBar.setHidden(False)
        self.progressBar.setMaximum(len(next(os.walk(self.fileloc))[2]))

        # for testing - todo: allow user to input correct answers
        answers = {0: 2, 1: 4, 2: 4, 3: 1, 4: 2, 5: 3, 6: 3, 7: 0, 8: 0, 9: 3, 10: 1, 11: 2, 12: 1, 13: 2, 14: 4, 15: 1,
                   16: 1, 17: 0, 18: 2, 19: 4}

        for subdir, dirs, files in os.walk(self.fileloc):
            for file in files:

                filepath = subdir + os.sep + file

                if filepath.endswith(".png") or filepath.endswith(".jpg") or filepath.endswith(".jpeg"):
                    try:
                        qr_info = (str(improcessing.find_qr(filepath)) + " ") * 3 + "1 1 1"
                        qr_info = qr_info.split(" ")

                        if qr_info[0] == qr_info[1] == qr_info[2] and qr_info[3] == qr_info[4] == qr_info[5]:
                            mark = improcessing.mark_answers(answers, filepath)
                            self.Results.add([qr_info[0], mark, qr_info[4]])
                        else:
                            # todo: handle qr code corruption better
                            print("qr code corrupted")

                        self.progressBar.setValue(self.progressBar.value() + 1)

                    except Exception as e:
                        # testing for any unexpected errors
                        print(e)

                else:
                    self.error = Dialog("error", "Error marking", "Unsupported file type")
                    self.error.show()
                    self.progressBar.setHidden(True)
                    break

            else:
                self.w.append(Dialog("notification", "All papers marked",
                                     "Tests have been marked, \nview them in the test section"))
                self.w[-1].show()

                if self.w[-1].exec_():
                    self.close()


class Dialog(QDialog):
    def __init__(self, type, title, text, parent=None):
        try:
            super().__init__()
            uic.loadUi("interface/UI/confirm_dialog.ui", self)

            self.title = title
            self.text = text

            if type == "error":
                self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
                self.logo = QPixmap("interface/UI/exclamation-icon.png")
            elif type == "confirm":
                self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Yes | QtWidgets.QDialogButtonBox.No)
                self.logo = QPixmap("interface/UI/question-icon.png")
            elif type == "notification":
                self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
                self.logo = QPixmap("interface/UI/thumbsup-icon.png")

            # Set up the user interface from Designer.
            self.text_title.setText(self.title)
            self.text_warning.setText(self.text)

            # add main logo to image
            self.icon.setPixmap(self.logo)
            self.icon.setScaledContents(True)

        except Exception as e:
            print(e)
