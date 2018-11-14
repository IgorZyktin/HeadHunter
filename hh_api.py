# -*- coding: utf-8 -*-
import json
import requests
import resp

LOCAL_MODE = True


def get_data(keyword: str, area: int):
    """
    Обработчик обращений к данным
    """
    if LOCAL_MODE:
        return load_local_vacancies(keyword, area)
    else:
        return load_remote_vacancies(keyword, area)


def _request(method, parameters=None):
    """
    Отправка запроса к API HH.ru
    """
    resp.save(f'Обращение к API HH. parameters = {parameters}', level=1)

    if parameters:
        request = requests.get(method, parameters)
    else:
        request = requests.get(method)

    status_code = request.status_code

    # нормальный режим
    if status_code == 200:
        return request.json()

    elif status_code == 400:
        resp.save(f'Ошибка 400: Некорректный запрос. parameters = {parameters}', level=3)
        argument = request.json().get("bad_argument")
        if argument:
            resp.save('Неправильный аргумент:' + str(argument), level=3)
    else:
        resp.save(f'Статус {status_code}: запрос не выполнен', level=3)
    return {}


def load_remote_vacancies(keyword: str = 'python', area: int = 1):
    """
    Поисковый запрос на сайте HH.ru
    """
    resp.save(f'Загрузка данных из интернета по запросу {keyword} в зоне {area}', level=1)

    # по идее должны скачиваться файлы на страницах [0, pages)
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


def load_local_vacancies(keyword: str = 'python', area: int = 1):
    """
    Загрузка данных из локальной базы
    """
    resp.save(f'Загрузка данных из локальной базы по запросу {keyword} в зоне {area}', level=1)
    with open(r'db\python.json', mode='r', encoding='utf-8') as file:
        result = json.load(file)
    return result


def load_vacancy_detailed(vacancy_id):
    """
    Загрузка подробных данных о конкретной вакансии с сайта
    """
    resp.save(f'Запрос подробного описания вакансии {vacancy_id} с сайта hh.ru', level=2)
    result = _request(method=f'https://api.hh.ru/vacancies/{vacancy_id}')
    return result
