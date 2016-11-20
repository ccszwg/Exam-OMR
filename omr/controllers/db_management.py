import csv


class Table(object):
    def __init__(self, name, table_type):
        self.name = name
        self.fieldnames = self.choose_field_names(table_type)

    def choose_field_names(self, table_type):
        if table_type == "class":
            return ["Student_ID", "Student_Name"]
        elif table_type == "results":
            return ["Class_Name", "Test_ID", "Student_ID", "Score"]
        elif table_type == "results":
            return ["Class_Name", "Test_ID", "Student_ID", "Score"]

    def create_table(self):
        with open("../data/" + self.name + ".csv", "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)

            writer.writeheader()

    def add_to_table(self, data):
        """
        PARAMS: student_data: {Student_ID: INT, Student_Name: STRING}
                results_data: {Class_Name: STRING, Student_ID: INT, Test_ID: INT, Score:INT}
                test_data:    {Test_ID: INT, Test_Name: STRING, Max_Mark: INT}
        """

        with open("../data/" + self.name + ".csv", "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.name)

            writer.writerow(data)
