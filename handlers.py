# -*- coding: utf-8 -*-
"""

    Модуль обработчиков
    Основная проблема - непредсказуемость наличия или отсутствия полей в вакансии
    Часто вречаются поля с None, пустые поля, поля с пустой строкой или нулём

"""
from collections import namedtuple
import datetime
dummy = 'Нет данных'

EUR_COURSE = 74.3
USD_COURSE = 65.1

# поправка на 13% подоходного налога
GROSS_COURSE = 0.87

DateClass = namedtuple('DateClass', ['created_at', 'published_at', 'edited_at'])
SalaryClass = namedtuple('SalaryClass', ['salary_from', 'salary_to', 'avg_salary', 'str_salary'])
InfoClass = namedtuple('InfoClass', ['experience', 'key_skills', 'description', 'short'])
AddressClass = namedtuple('AddressClass', ['city', 'street'])
EmployerClass = namedtuple('EmployerClass', ['employer_id', 'employer_name',
                                             'employer_url', 'employer_logo'])


def handle_location(raw_data):
    """
        Обработчик адреса
    """
    city = None
    street = None

    if raw_data is None:
        return AddressClass(None, None)

    if 'address' in raw_data:
        temp = raw_data['address']

        if temp is not None and 'city' in temp:
            if temp['city']:
                city = temp['city']

        if temp is not None and 'street' in temp:
            if temp['street']:
                street = temp['street']

    return AddressClass(city, street)


def handle_salary(raw_data):
    """
        Обработчик зарплаты
    """
    salary_to = None
    salary_from = None
    gross = None
    currency = None

    if raw_data is None:
        return SalaryClass(None, None, 0, dummy)

    if 'salary' in raw_data:

        temp = raw_data['salary']
        if temp is not None and 'from' in temp:
            if temp['from']:
                salary_from = int(temp['from'])

        if temp is not None and 'to' in temp:
            if temp['to']:
                salary_to = int(temp['to'])

        if temp is not None and 'gross' in temp:
            if temp['gross']:
                gross = bool(temp['gross'])

        if temp is not None and 'currency' in temp:
            if temp['currency']:
                currency = temp['currency']

    if currency == 'USD':
        scale = USD_COURSE
    elif currency == 'EUR':
        scale = EUR_COURSE
    elif currency == 'RUR':
        scale = 1
    else:
        # TODO - добавить дополнительные валюты
        scale = -1

    if gross:
        scale = scale * GROSS_COURSE

    if salary_from:
        salary_from = int(salary_from * scale)

    if salary_to:
        salary_to = int(salary_to * scale)

    if salary_from and salary_to:
        str_salary = f'{salary_from//1000}к-{salary_to//1000}к'.center(9)
        avg_salary = int((salary_from + salary_to) / 2)

    elif salary_from and not salary_to:
        str_salary = f'от {salary_from//1000}к'.center(9)
        avg_salary = salary_from

    elif not salary_from and salary_to:
        str_salary = f'до {salary_to}к'.center(9)
        avg_salary = salary_to
    else:
        str_salary = dummy
        avg_salary = 0

    return SalaryClass(salary_from, salary_to, avg_salary, str_salary)


def handle_info(raw_data):
    """
        Обработчик основных данных о вакансии
    """
    description = None
    experience = None
    key_skills = None
    short = ''

    if raw_data is None:
        return InfoClass(None, None, None, None)

    if 'description' in raw_data:
        if raw_data['description']:
            description = raw_data['description']

    if 'experience' in raw_data:
        if raw_data['experience']:
            experience = raw_data['experience']

    if 'key_skills' in raw_data and raw_data['key_skills']:
        raw_key_skills = raw_data['key_skills']
        if isinstance(raw_key_skills, list):
            names = [x.get('name', '') for x in raw_key_skills]
            key_skills = ', '.join(names)

    if 'snippet' in raw_data and raw_data['snippet']:
        snippet = raw_data['snippet']

        if 'requirement' in snippet:
            if snippet['requirement']:
                requirement = snippet['requirement'].replace('<highlighttext>', '')
                short += requirement

        if 'responsibility' in snippet:
            if snippet['responsibility']:
                responsibility = snippet['responsibility'].replace('<highlighttext>', '')
                short += ' ' + responsibility

    return InfoClass(experience, key_skills, description, short or None)


def handle_employer(raw_data):
    """
        Обработчик работодателя
    """
    employer_id = None
    employer_name = None
    employer_url = None
    employer_logo = None

    if raw_data is None:
        return EmployerClass(None, None, None, None)

    if 'employer' in raw_data:
        employer = raw_data['employer']
        if employer and 'id' in employer:
            if employer['id']:
                employer_id = int(employer['id'])

        if employer and 'name' in employer:
            if employer['name']:
                employer_name = employer['name']

        if employer and 'alternate_url' in employer:
            if employer['alternate_url']:
                employer_url = employer['alternate_url']

        if employer and 'logo_urls' in employer:
            if isinstance(employer['logo_urls'], dict):
                employer_logo = employer['logo_urls'].get('original')

    return EmployerClass(employer_id, employer_name, employer_url, employer_logo)


def handle_date(raw_data):
    """
    Обработчик времени
    """
    if raw_data is None:
        return DateClass(None, None, None)

    created_at = None
    if 'created_at' in raw_data:
        if raw_data['created_at']:
            temp = raw_data['created_at']
            created_at = datetime.datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S+%f").timestamp()

    published_at = None
    if 'published_at' in raw_data:
        if raw_data['published_at']:
            temp = raw_data['published_at']
            published_at = datetime.datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S+%f").timestamp()

    edited_at = None
    if 'edited_at' in raw_data:
        if raw_data['edited_at']:
            temp = raw_data['edited_at']
            edited_at = datetime.datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S+%f").timestamp()

    return DateClass(created_at, published_at, edited_at)


