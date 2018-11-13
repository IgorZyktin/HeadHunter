"""
    Модуль обработки вакансий
"""
from colorama import init, Fore
init(autoreset=True)

EUR_COURSE = 74.3
USD_COURSE = 65.1
GROSS_COURSE = 0.87


def extract_valid_data(raw_vacancy: dict) -> dict:
    """
    Производит обработку исходных данных, генерируя на выходе
    словарь со стандартизованными полями
    Сюда приходит метод add_vacancy из класса VacancyManager
    """
    filthered_vacancy = dict()

    # сама вакансия
    filthered_vacancy['id'] = raw_vacancy.get('id')
    filthered_vacancy['name'] = raw_vacancy.get('name')
    filthered_vacancy['url'] = raw_vacancy.get('alternate_url')
    filthered_vacancy['date'] = raw_vacancy.get('published_at')
    filthered_vacancy['responsibility'] = None
    filthered_vacancy['requirement'] = None

    # работодатель
    filthered_vacancy['employer_name'] = None
    filthered_vacancy['employer_url'] = None

    # местоположение
    filthered_vacancy['area'] = None
    filthered_vacancy['metro'] = None

    # зарплата
    filthered_vacancy['salary_from'] = 0
    filthered_vacancy['salary_to'] = 0
    filthered_vacancy['gross'] = None
    filthered_vacancy['currency'] = None

    if 'salary' in raw_vacancy and raw_vacancy['salary']:
        actual_from = raw_vacancy['salary'].get('from')
        if actual_from:
            filthered_vacancy['salary_from'] = actual_from
        actual_to = raw_vacancy['salary'].get('to')
        if actual_to:
            filthered_vacancy['salary_to'] = actual_to
        filthered_vacancy['gross'] = raw_vacancy['salary'].get('gross')
        filthered_vacancy['currency'] = raw_vacancy['salary'].get('currency')

    if 'employer' in raw_vacancy and raw_vacancy['employer']:
        filthered_vacancy['employer_name'] = raw_vacancy['employer'].get('name')
        filthered_vacancy['employer_url'] = raw_vacancy['employer'].get('alternate_url')

    if 'area' in raw_vacancy and raw_vacancy['area']:
        filthered_vacancy['area'] = raw_vacancy.get('area')

    if 'snippet' in raw_vacancy and raw_vacancy['snippet']:
        filthered_vacancy['responsibility'] = raw_vacancy.get('responsibility')
        filthered_vacancy['requirement'] = raw_vacancy.get('requirement')

    if 'address' in raw_vacancy and raw_vacancy['address']:
        filthered_vacancy['metro'] = raw_vacancy['address'].get('metro')
    return filthered_vacancy


def str_sal(starting: int, ending: int, currency: str, gross: bool) -> str:
    """
    Генерация строкового представления зарплаты для удобного отображения на экране
    Сюда приходит метод str_salary из класса Vacancy
    """
    str_salary = ''

    if currency == 'USD' or currency == 'EUR':
        str_currency = ' ' + currency
        space = '-'
    else:
        str_currency = ''
        space = ' - '

    if gross:
        gross_koeff = GROSS_COURSE
    else:
        gross_koeff = 1

    salary_from = int((starting / 1000) * gross_koeff)
    salary_to = int((ending / 1000) * gross_koeff)

    if salary_from and salary_to:
        str_salary = str(salary_from) + 'к' + space + str(salary_to) + 'к' + str_currency

    elif salary_from and not salary_to:
        str_salary = 'от ' + str(salary_from) + 'к' + str_currency

    elif not salary_from and salary_to:
        str_salary = 'до ' + str(salary_to) + 'к' + str_currency

    return Fore.RED + str_salary.center(11) + Fore.RESET


def avg_sal(starting: int, ending: int, currency: str, gross: bool) -> int:
    """
    Генерация числового выражения зарплаты для сортировки вакансий
    Сюда приходит метод avg_salary из класса Vacancy
    """
    if currency == 'USD':
        currency_koef = USD_COURSE
    elif currency == 'EUR':
        currency_koef = EUR_COURSE
    else:
        currency_koef = 1

    if gross:
        gross_koeff = GROSS_COURSE
    else:
        gross_koeff = 1

    actual_starting = starting * currency_koef * gross_koeff
    actual_ending = ending * currency_koef * gross_koeff

    if actual_starting and actual_ending:
        num = (actual_starting + actual_ending) / 2

    elif not actual_starting and actual_ending:
        num = actual_ending

    elif actual_starting and not actual_ending:
        num = actual_starting
    else:
        num = 0

    return int(num)


def make_str_vacancy(vacancy_id: str, vacancy_name: str, ) -> str:
    """
    Строковое представление вакансии
    Сюда приходит метод __str__ из класса Vacancy
    """
    colored_vacancy_id = Fore.CYAN + str(vacancy_id) + Fore.RESET
    colored_vacancy_name = Fore.YELLOW + vacancy_name[:41]
    return colored_vacancy_id + ' ' + colored_vacancy_name
