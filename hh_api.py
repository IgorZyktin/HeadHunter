import json
import requests
from colorama import init, Fore
init(autoreset=True)


def _ask_hh_api(parameters):
    """
    Отправка запроса к API HH.ru
    """
    request = requests.get('https://api.hh.ru/vacancies/', parameters)
    status_code = request.status_code
    request_dict = request.json()

    # нормальный режим
    if status_code == 200:
        return request_dict

    elif status_code == 400:
        print(Fore.RED + f'Ошибка 400: Некорректный запрос.')
        argument = request_dict.get("bad_argument")
        if argument:
            print(Fore.RED + 'Неправильный аргумент:' + str(argument))

    elif status_code == 403:
        print(Fore.RED + 'Ошибка 403: Ошибка прав доступа.')
    elif status_code == 404:
        print(Fore.RED + 'Ошибка 404: Страница не найдена.')
    elif status_code == 429:
        print(Fore.RED + 'Ошибка 429: Превышен лимит просмотров.')
    elif status_code == 500:
        print(Fore.RED + 'Ошибка 500: Нет доступа.')
    elif status_code == 503:
        print(Fore.RED + 'Ошибка 503: Нет доступа.')
    return {}


def retrieve_vacancies(keyword, local=True):
    """
    Скачивание данных из базы HH.ru
    Ответ приходит в виде json-файла, в котором нас интересует поле items
    """
    storage = []
    if local:
        # имитация загрузки
        with open('python.json', mode='r', encoding='utf-8-sig') as file:
            storage = json.load(file)
    else:
        # по идее должны счкачиваться файлы на страницах [0, pages)
        # но данные последней никак не получается достать (возможно ошибка API)
        area = 1        # Москва
        per_page = 50   # Вакансий в странице

        parameters = {'text': keyword, 'area': area, 'per_page': per_page, 'page': 0}
        request = _ask_hh_api(parameters)

        storage.extend(request.get('items'))
        pages = request.get('pages', 0)
        for page in range(pages):
            parameters = {'text': keyword, 'area': area, 'per_page': per_page, 'page': page}
            request = _ask_hh_api(parameters)
            storage.extend(request.get('items', []))

    return storage
