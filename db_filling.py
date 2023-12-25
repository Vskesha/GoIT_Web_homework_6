from datetime import date, datetime, timedelta
from faker import Faker
from random import randint
import sqlite3

disciplines = {
    'математика',
    'література',
    'англійська',
    'історія',
    'географія',
    'біологія',
    'хімія',
    'фізика',
}

groups = ['БЛБ-31', 'БЛБ-32', 'БЛБ-33']
NUMBER_OF_TEACHERS = 5
NUMBER_OF_STUDENTS = 50
fake = Faker('uk-UA')
connect = sqlite3.connect('university.db')
cur = connect.cursor()


def fill_teachers():
    teachers = [fake.name() for _ in range(NUMBER_OF_TEACHERS)]
    sql = "INSERT INTO teachers(fullname) VALUES(?);"
    cur.executemany(sql, zip(teachers, ))


def fill_disciplines():
    sql = "INSERT INTO disciplines(name, teacher_id) VALUES(?, ?);"
    cur.executemany(sql, zip(disciplines, iter(randint(1, NUMBER_OF_TEACHERS) for _ in disciplines)))


def fill_groups():
    sql = "INSERT INTO groups(name) VALUES(?);"
    cur.executemany(sql, zip(groups, ))


def fill_students():
    students = [fake.name() for _ in range(NUMBER_OF_STUDENTS)]
    sql = "INSERT INTO students(fullname, group_id) VALUES(?, ?);"
    cur.executemany(sql, zip(students, iter(randint(1, len(groups)) for _ in students)))


def fill_grades():
    start_date = datetime.strptime("2022-09-01", "%Y-%m-%d").date()
    end_date = datetime.strptime("2023-06-15", "%Y-%m-%d").date()
    sql = "INSERT INTO grades(discipline_id, student_id, grade, date_of) VALUES(?, ?, ?, ?);"

    list_dates = get_list_of_dates(start_date, end_date)

    grades = []
    for day in list_dates:
        random_discipline = randint(1, len(disciplines))
        random_students = [randint(1, NUMBER_OF_STUDENTS) for _ in range(5)]
        for student in random_students:
            grades.append((random_discipline, student, randint(1, 12), day))
    cur.executemany(sql, grades)


def get_list_of_dates(start: date, end: date):
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


if __name__ == "__main__":
    try:
        fill_teachers()
        fill_disciplines()
        fill_groups()
        fill_students()
        fill_grades()
        connect.commit()
    except sqlite3.Error as error:
        print(error)
    finally:
        connect.close()
