# -*- coding: utf-8 -*-
"""

    Модуль обработчиков
    Основная проблема - непредсказуемость наличия или отсутствия полей в вакансии
    Часто вречаются поля с None, пустые поля, поля с пустой строкой или нулём

"""
from collections import namedtuple
import datetime
import math
import time
import re

EUR_COURSE = 74.3
USD_COURSE = 65.1

# поправка на 13% подоходного налога
GROSS_COURSE = 0.87

"""
Перечень всех атрибутов (имена поддерживают сортировку):
attr_04_salary_from: int | None - минимальная зарплата в килорублях
attr_05_salary_upto: int | None - максимальная зарплата в килорублях
attr_06_salary_avg_: int -------- средняя зарплата в килорублях или 0
attr_07_salary_str_: str -------- текстовое представление зарплаты вида "999к-999к" или 'Нет данных'

attr_08_experience_: str | None - требуемый опыт
attr_09_key_skills_: str | None - требуемые навыки
attr_10_description: str | None - подробное описание (доступно по отдельному запросу)
attr_11_short_descr: str | None - описание по первичному запросу (обрывается на полуслове)

attr_12_employer_id__: int | None - уникальный id работодателя
attr_13_employer_url_: str | None - адрес страницы работодателя
attr_14_employer_name: str | None - название организации работодателя

attr_15_time_created: float | None - время создания вакансии
attr_16_time_publish: float | None - время публикации вакансии
attr_17_time_dbsaved: float -------- прошлый сеанс обработки, заполнен всегда

attr_18_addr_city__: str | None - город работодателя
attr_19_addr_street: str | None - улица работодателя (многие в этом поле пишут ветку метро)
"""

SalaryClass = namedtuple('SalaryClass', ['attr_04_salary_from',
                                         'attr_05_salary_upto',
                                         'attr_06_salary_avg_',
                                         'attr_07_salary_str_'])

InfoClass = namedtuple('InfoClass', ['attr_08_experience_',
                                     'attr_09_key_skills_',
                                     'attr_10_description',
                                     'attr_11_short_descr'])

EmployerClass = namedtuple('EmployerClass', ['attr_12_employer_id__',
                                             'attr_13_employer_url_',
                                             'attr_14_employer_name'])

TimeClass = namedtuple('TimeClass', ['attr_15_time_created',
                                     'attr_16_time_publish',
                                     'attr_17_time_dbsaved'])

AddressClass = namedtuple('AddressClass', ['attr_18_addr_city__',
                                           'attr_19_addr_street'])


def handle_salary(raw_data: dict) -> namedtuple:
    """
        Обработчик зарплаты
    """
    if raw_data is None:
        return SalaryClass(None, None, 0, 'Нет данных')

    attr_04_salary_from = None
    attr_05_salary_upto = None

    _gross = None
    _currency = None

    if 'salary' in raw_data:

        temp = raw_data['salary']
        if temp is not None and 'from' in temp:
            if temp['from']:
                attr_04_salary_from = int(temp['from'])

        if temp is not None and 'to' in temp:
            if temp['to']:
                attr_05_salary_upto = int(temp['to'])

        if temp is not None and 'gross' in temp:
            if temp['gross']:
                _gross = bool(temp['gross'])

        if temp is not None and 'currency' in temp:
            if temp['currency']:
                _currency = temp['currency']

    if _currency == 'USD':
        scale = USD_COURSE
    elif _currency == 'EUR':
        scale = EUR_COURSE
    elif _currency == 'RUR':
        scale = 1
    else:
        # TODO - добавить дополнительные валюты
        scale = -1

    if _gross:
        scale = scale * GROSS_COURSE

    if attr_04_salary_from:
        attr_04_salary_from = int(math.floor(attr_04_salary_from * scale))

    if attr_05_salary_upto:
        attr_05_salary_upto = int(math.floor(attr_05_salary_upto * scale))

    if attr_04_salary_from and attr_05_salary_upto:
        attr_07_salary_str_ = f'{attr_04_salary_from//1000}к-{attr_05_salary_upto//1000}к'.center(9)
        attr_06_salary_avg_ = int((attr_04_salary_from + attr_05_salary_upto) / 2)

    elif attr_04_salary_from and not attr_05_salary_upto:
        attr_07_salary_str_ = f'от {attr_04_salary_from//1000}к'.center(9)
        attr_06_salary_avg_ = attr_04_salary_from

    elif not attr_04_salary_from and attr_05_salary_upto:
        attr_07_salary_str_ = f'до {attr_05_salary_upto//1000}к'.center(9)
        attr_06_salary_avg_ = attr_05_salary_upto
    else:
        attr_07_salary_str_ = 'Нет данных'
        attr_06_salary_avg_ = 0

    return SalaryClass(attr_04_salary_from,
                       attr_05_salary_upto,
                       attr_06_salary_avg_,
                       attr_07_salary_str_)


def handle_info(raw_data: dict) -> namedtuple:
    """
        Обработчик основных данных о вакансии
    """
    attr_10_description = None
    attr_08_experience_ = None
    attr_09_key_skills_ = None
    attr_11_short_descr = ''

    if raw_data is None:
        return InfoClass(None, None, None, None)

    if 'description' in raw_data:
        if raw_data['description']:
            attr_10_description = raw_data['description']

    if 'experience' in raw_data:
        if raw_data['experience']:
            attr_08_experience_ = raw_data['experience']

    if 'key_skills' in raw_data and raw_data['key_skills']:
        raw_key_skills = raw_data['key_skills']
        if isinstance(raw_key_skills, list):
            skills = []
            for skill in raw_key_skills:
                if isinstance(skill, dict):
                    new_skill = skill.get('name')
                    if new_skill:
                        skills.append(skill.get('name'))
            if skills:
                attr_09_key_skills_ = ', '.join(skills)

    if 'snippet' in raw_data and raw_data['snippet']:
        snippet = raw_data['snippet']

        if 'requirement' in snippet:
            if snippet['requirement']:
                pattern = r'<.?highlighttext>'
                requirement = snippet['requirement']
                requirement = re.sub(pattern, '', requirement)
                attr_11_short_descr += requirement

        if 'responsibility' in snippet:
            if snippet['responsibility']:
                pattern = r'<.?highlighttext>'
                responsibility = snippet['responsibility']
                responsibility = re.sub(pattern, '', responsibility)
                attr_11_short_descr += ' ' + responsibility

    return InfoClass(attr_08_experience_,
                     attr_09_key_skills_,
                     attr_10_description,
                     attr_11_short_descr or None)


def handle_employer(raw_data: dict) -> namedtuple:
    """
        Обработчик работодателя
    """
    if raw_data is None:
        return EmployerClass(None, None, None)

    attr_12_employer_id__ = None
    attr_14_employer_name = None
    attr_13_employer_url_ = None

    if 'employer' in raw_data:
        employer = raw_data['employer']
        if employer and 'id' in employer:
            if employer['id']:
                attr_12_employer_id__ = int(employer['id'])

        if employer and 'name' in employer:
            if employer['name']:
                attr_14_employer_name = employer['name']

        if employer and 'alternate_url' in employer:
            if employer['alternate_url']:
                attr_13_employer_url_ = employer['alternate_url']

    return EmployerClass(attr_12_employer_id__, attr_13_employer_url_, attr_14_employer_name)


def handle_time(raw_data: dict) -> namedtuple:
    """
    Обработчик времени
    """
    attr_17_time_dbsaved = time.time()
    if raw_data is None:
        return TimeClass(None, None, attr_17_time_dbsaved)

    attr_15_time_created = None
    if 'created_at' in raw_data:
        if raw_data['created_at']:
            temp = raw_data['created_at']
            try:
                attr_15_time_created = datetime.datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S+%f")
                attr_15_time_created = attr_15_time_created.timestamp()
            except ValueError:
                pass

    attr_16_time_publish = None
    if 'published_at' in raw_data:
        if raw_data['published_at']:
            temp = raw_data['published_at']
            try:
                attr_16_time_publish = datetime.datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S+%f")
                attr_16_time_publish = attr_16_time_publish.timestamp()
            except ValueError:
                pass

    return TimeClass(attr_15_time_created, attr_16_time_publish, attr_17_time_dbsaved)


def handle_location(raw_data: dict) -> namedtuple:
    """
        Обработчик адреса
    """
    if raw_data is None:
        return AddressClass(None, None)

    attr_18_addr_city__ = None
    attr_19_addr_street = None

    if 'address' in raw_data:
        temp = raw_data['address']

        if temp is not None and 'city' in temp:
            if temp['city']:
                attr_18_addr_city__ = temp['city']

        if temp is not None and 'street' in temp:
            if temp['street']:
                attr_19_addr_street = temp['street']

    if not attr_18_addr_city__:
        if 'area' in raw_data and raw_data['area'] is not None:
            attr_18_addr_city__ = raw_data['area'].get('name')

    return AddressClass(attr_18_addr_city__, attr_19_addr_street)
