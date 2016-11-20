import sqlite3


def scrub(table_name):
    if isinstance(table_name, str):
        return ''.join(chr for chr in table_name if chr.isalnum() or chr == " ")
    else:
        return table_name


def generate_database():
    conn = sqlite3.connect("../data/database.db")

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


def add_class(class_data):
    if not isinstance(class_data, tuple) or len(class_data) != 1:
        raise TypeError("Expected 1-tuple")

    conn = sqlite3.connect("../data/database.db")

    c = conn.cursor()

    class_data = tuple([scrub(i) for i in list(class_data)])
    print(class_data)

    c.execute('INSERT INTO Classes(Class_Name) VALUES (?)', class_data)

    conn.commit()
    conn.close()


def add_student(student_data):
    if not isinstance(student_data, tuple) or len(student_data) != 2:
        raise TypeError("Expected 2-tuple")

    conn = sqlite3.connect("../data/database.db")

    c = conn.cursor()

    student_data = tuple([scrub(i) for i in list(student_data)])
    print(student_data)

    c.execute('INSERT INTO Students(Student_Name, Class_ID) VALUES (?,?)', student_data)

    conn.commit()
    conn.close()


def add_result(result_data):
    if not isinstance(result_data, tuple) or len(result_data) != 3:
        raise TypeError("Expected 3-tuple")

    conn = sqlite3.connect("../data/database.db")

    c = conn.cursor()

    result_data = tuple([scrub(i) for i in list(result_data)])
    print(result_data)

    c.execute('INSERT INTO Results(Student_ID, Score, Test_ID) VALUES (?,?, ?)', result_data)

    conn.commit()
    conn.close()


def add_test(test_data):
    if not isinstance(test_data, tuple) or len(test_data) != 2:
        raise TypeError("Expected 2-tuple")

    conn = sqlite3.connect("../data/database.db")

    c = conn.cursor()

    test_data = tuple([scrub(i) for i in list(test_data)])
    print(test_data)

    c.execute('INSERT INTO Tests(Test_Name, Max_score) VALUES (?,?)', test_data)

    conn.commit()
    conn.close()
