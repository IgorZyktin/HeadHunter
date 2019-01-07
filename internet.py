# -*- coding: utf-8 -*-
import requests


def _request(method, parameters=None):
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
