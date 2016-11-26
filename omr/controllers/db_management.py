import sqlite3


def scrub(table_name):
    try:
        return int(table_name)
    except ValueError:
        if isinstance(table_name, str):
            return "'%s'" % ''.join(chr for chr in table_name if chr.isalnum() or chr == " ")
        else:
            return table_name


class Table(object):
    def __init__(self, table):
        self.table = table
        self.headers = self.create_headers()
        self.primarykey = self.create_primarykeys()

        self.generate_database()

    def create_headers(self):
        if self.table == "Classes":
            return "Class_Name"
        elif self.table == "Students":
            return "Student_Name, Class_ID"
        elif self.table == "Results":
            return "Student_ID, Score, Test_ID"
        elif self.table == "Tests":
            return "Test_Name, Max_score"
        else:
            raise AttributeError("Table parameter is not understood")

    def create_primarykeys(self):
        if self.table == "Classes":
            return "Class_ID"
        elif self.table == "Students":
            return "Student_ID"
        elif self.table == "Results":
            return "Results_ID"
        elif self.table == "Tests":
            return "Test_ID"
        else:
            raise AttributeError("Table parameter is not understood")

    def generate_database(self):
        conn = sqlite3.connect("data/database.db")

        c = conn.cursor()

        c.execute("create table if not exists Classes ("
                  "Class_ID INTEGER PRIMARY KEY, "
                  "Class_Name TEXT)")

        c.execute("create table if not exists Students ("
                  "Student_ID INTEGER PRIMARY KEY, "
                  "Student_Name TEXT, "
                  "Class_ID INTEGER)")

        c.execute("create table if not exists Results ("
                  "Results_ID INTEGER PRIMARY KEY, "
                  "Student_ID TEXT, "
                  "Score INTEGER, "
                  "Test_ID INTEGER)")

        c.execute("create table if not exists Tests ("
                  "Test_ID INTEGER PRIMARY KEY, "
                  "Test_Name TEXT, "
                  "Max_score INTEGER)")

        conn.close()

    def name_exists(self, name, additional_criteria=""):

        conn = sqlite3.connect("data/database.db")

        c = conn.cursor()
        c.execute("SELECT rowid FROM " + self.table + " WHERE " + self.headers.split(", ")[0] + '="' + name + '"' +
                  additional_criteria)
        data = c.fetchall()

        conn.commit()
        conn.close()

        if len(data) == 0:
            # no names found
            return False
        else:
            return True

    def add(self, data):

        conn = sqlite3.connect("data/database.db")

        c = conn.cursor()

        data = [scrub(i) for i in data]

        # todo: REFACTOR BELOW

        if len(data) == 1:
            c.execute("INSERT INTO " + self.table + " (" + self.headers + ") " + ' VALUES (' + data[0] + ')')
        else:
            c.execute("INSERT INTO " + self.table + " (" + self.headers + ") " + " VALUES (" + ", ".join(
                list(map(str, data))) + ")")

        conn.commit()
        conn.close()

    def get_names(self, criteria=""):
        conn = sqlite3.connect("data/database.db")

        c = conn.cursor()
        c.execute("SELECT " + self.headers.split(", ")[0] + " FROM " + self.table + criteria)
        data = c.fetchall()

        conn.commit()
        conn.close()

        return data

    def get_ID(self, criteria=""):
        conn = sqlite3.connect("data/database.db")

        c = conn.cursor()
        c.execute("SELECT " + self.primarykey + " FROM " + self.table + criteria)
        data = c.fetchall()

        conn.commit()
        conn.close()

        return data
