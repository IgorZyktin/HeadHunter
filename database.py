"""

    Модуль взаимодействия с базой данных

"""
import sqlite3
from sqlite3 import Error


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
        db_data.append((vacancy.id,
                        vacancy.name,
                        vacancy.url,
                        vacancy.description,
                        vacancy.experience,
                        vacancy.key_skills,
                        vacancy.short,
                        vacancy.published_at,
                        vacancy.created_at,
                        vacancy.edited_at,
                        vacancy.salary_from,
                        vacancy.salary_to,
                        vacancy.avg_salary,
                        vacancy.str_salary,
                        vacancy.city,
                        vacancy.street,
                        vacancy.employer_id,
                        vacancy.employer_name,
                        vacancy.employer_url,
                        vacancy.employer_logo
                        ))

    conn = create_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS main (id integer, 
                                                        name text,
                                                        url text,
                                                        description text,
                                                        experience text,
                                                        key_skills text,
                                                        short text,
                                                        published_at float, 
                                                        created_at float,
                                                        edited_at float,
                                                        salary_from integer,
                                                        salary_to integer,
                                                        avg_salary integer,
                                                        str_salary text,
                                                        city text,
                                                        street text,
                                                        employer_id integer,
                                                        employer_name text,
                                                        employer_url text,
                                                        employer_logo text
                                                        )""")
        for line in db_data:
            cursor.executemany("INSERT INTO main VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (line,))
        conn.commit()
        return



def main():
    """
        Главная функция
    """
    pass



if __name__ == '__main__':
    main()
