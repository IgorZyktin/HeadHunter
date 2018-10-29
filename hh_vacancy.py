"""
    В этом модуле находится класс вакансии и его обработчик
"""
import hh_processing
import operator
from colorama import init, Fore
init(autoreset=True)


class Vacancy:
    """
    Главный класс всех вакансий.
    Выступает основным хранилищем данных
    """
    def __init__(self, data):
        self.id = data['id']
        self.url = data['url']
        self.name = data['name']
        self.date = data['date']
        self.area = data['area']
        self.metro = data['metro']
        self.gross = data['gross']
        self.currency = data['currency']
        self.salary_to = data['salary_to']
        self.requirement = data['requirement']
        self.salary_from = data['salary_from']
        self.employer_url = data['employer_url']
        self.employer_name = data['employer_name']
        self.responsibility = data['responsibility']

    def __str__(self):
        return hh_processing.make_str_vacancy(self.id, self.name)

    @property
    def str_salary(self):
        return hh_processing.str_sal(self.salary_from, self.salary_to, self.currency, self.gross)

    @property
    def avg_salary(self):
        return hh_processing.avg_sal(self.salary_from, self.salary_to, self.currency, self.gross)

    @property
    def has_salary(self):
        return self.avg_salary != 0


class VacancyManager:
    """
    Класс-обработчик для Vacancy.
    Организует взаимодействие остальной программы с классом вакансий
    """
    memory = []

    @staticmethod
    def initiate(raw_data):
        # генерация новых экземпляров вакансий из списка json-словарей
        for raw_vacancy in raw_data:
            VacancyManager.add_vacancy(raw_vacancy)
        VacancyManager.memory.sort(key=operator.attrgetter('avg_salary'))

    @staticmethod
    def add_vacancy(raw_vacancy):
        # генерация одного нового экземпляра вакансии из json-словаря
        vacancy_dict = hh_processing.extract_valid_data(raw_vacancy)
        new_vacancy = Vacancy(vacancy_dict)
        VacancyManager.memory.append(new_vacancy)

    @staticmethod
    def get_vacancy(number):
        # получение вакансии из списка существующщих вакансий по индексу
        if 0 <= number <= len(VacancyManager.memory):
            return VacancyManager.memory[number]
        else:
            raise IndexError('Нет вакансии с таким номером')

    @staticmethod
    def show_all():
        # вывод всех сохранённых данных на экран
        total = len(VacancyManager.memory)
        digits = len(str(total))
        print(f'В памяти находится {total} записей:')
        for i, each in enumerate(VacancyManager.memory, start=1):
            num = str(i).rjust(digits, '0')
            print(f'\t{num}. {each}')

    @staticmethod
    def clear():
        # стереть всё содержимое
        for i in range(len(VacancyManager.memory)):
            del VacancyManager.memory[0]
        VacancyManager.memory.clear()
