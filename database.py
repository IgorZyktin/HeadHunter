"""

    Модуль взаимодействия с базой данных

"""
import sqlite3
from sqlite3 import Error
import vacancy as Vacancy
import responds


def create_connection(db_file=r"DB\headhunter.db"):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def dump(vacancies):
    """
    Сохранение набора вакансий в базу
    """
    db_data = []

    for vacancy in vacancies.values():
        print(vacancy)
        db_data.append([*vacancy.attribute_names()])

    names = ','.join(Vacancy.Vacancy.attribute_names())
    conn = create_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS main (?)""", (names,))
        for line in db_data:
            cursor.executemany("INSERT INTO main VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (line,))
        conn.commit()
        return


def drop_db():
    """
    Удаление таблицы
    """
    responds.save(f'Удаление таблицы базы данных', level=5)
    conn = create_connection()
    # with conn:
        # cursor = conn.cursor()
        # cursor.execute("""DROP TABLE address""")
        # return


def main():
    """
        Главная функция
    """
    pass



if __name__ == '__main__':
    main()
