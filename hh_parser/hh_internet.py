# -*- coding: utf-8 -*-
"""

    Модуль взаимодействия с интернетом

"""
from xml.etree import ElementTree
import requests


def _request(method: str, parameters=None) -> dict:
    """
    Отправка запроса к API HH.ru
    """
    if parameters:
        request = requests.get(method, parameters)
    else:
        request = requests.get(method)

    status_code = request.status_code

    if status_code == 200:
        return request.json()

    print('ОШИБКА Не удалось обработать запрос для', parameters)
    return {}


def load_vacancies(keyword: str = 'python', area: int = 1) -> list:
    """
    Поисковый запрос на сайте HH.ru
    """
    # по идее должны скачиваться файлы на страницах с 0 по pages
    # но данные последней никак не получается достать (возможно ошибка API)
    per_page = 50   # Вакансий в странице

    parameters = {'text': keyword, 'area': area, 'per_page': per_page, 'page': 0}
    request = _request('https://api.hh.ru/vacancies/', parameters)

    storage = []
    storage.extend(request.get('items'))
    pages = request.get('pages', 0)

    for page in range(pages):
        parameters = {'text': keyword, 'area': area, 'per_page': per_page, 'page': page}
        request = _request('https://api.hh.ru/vacancies/', parameters)
        storage.extend(request.get('items', []))

    return storage


def load_detailed(vacancy_id: int) -> dict:
    """
    Загрузка подробных данных о конкретной вакансии с сайта
    """
    result = _request(method=f'https://api.hh.ru/vacancies/{vacancy_id}')
    return result


def get_areas() -> dict:
    """
        Получение с сайта словаря с кодами городов
    """
    result = _request(method=f'https://api.hh.ru/areas')
    return result


# noinspection PyDefaultArgument
def get_course(currency: str, memory: dict = {}) -> float:
    """
        Получение курса валют
    """
    if not currency:
        return -1.0

    currency = currency.upper()

    if currency not in memory:
        request = requests.get(r'http://www.cbr.ru/scripts/XML_daily_eng.asp')

        if not request:
            print('Не удалось получить курсы валют с сайта cbr.ru')
            return -1.0

        currencies = ElementTree.fromstring(request.text)

        for currency_obj in currencies:
            name = ''
            value = 0.0
            for i, child in enumerate(currency_obj):
                if i == 1:
                    name = child.text
                if i == 4:
                    value = float(child.text.replace(',', '.'))
            memory[name] = value

    return memory.get(currency, -1.0)
