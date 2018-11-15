# -*- coding: utf-8 -*-
"""

    В этом модуле находится класс вакансии и его управляющий класс

"""
import handlers
import hh_api
import responds
import hh_html
import json


class Overlord:
    """
    Сборщик данных по созданным экземплярам
    """
    _memory = {}

    @staticmethod
    def add_manager(manager):
        Overlord._memory.update({manager.name: manager})

    @staticmethod
    def enlist_managers():
        for name, manager in Overlord._memory.items():
            print(name, manager.total())


class Vacancy:
    """
    Базовый класс вакансии
    """
    def __init__(self, raw_data):
        self.id = int(raw_data.get('id'))
        self.name = raw_data.get('name')
        self.url = raw_data.get('alternate_url')

        # self.raw_data = json.dumps(raw_data, ensure_ascii=False)

        new_info = handlers.handle_info(raw_data)
        self.description = new_info.description
        self.experience = new_info.experience
        self.key_skills = new_info.key_skills
        self.short = new_info.short

        new_date = handlers.handle_date(raw_data)
        self.created_at = new_date.created_at
        self.published_at = new_date.published_at
        self.edited_at = new_date.edited_at

        new_salary = handlers.handle_salary(raw_data)
        self.salary_from = new_salary.salary_from
        self.salary_to = new_salary.salary_to
        self.avg_salary = new_salary.avg_salary
        self.str_salary = new_salary.str_salary

        new_location = handlers.handle_location(raw_data)
        self.city = new_location.city
        self.street = new_location.street

        new_employer = handlers.handle_employer(raw_data)
        self.employer_id = new_employer.employer_id
        self.employer_name = new_employer.employer_name
        self.employer_url = new_employer.employer_url
        self.employer_logo = new_employer.employer_logo

    def __str__(self):
        return f'{self.id} {self.str_salary} {self.name}'

    def __repr__(self):
        return '[VAC] ' + str(self.id)

    def flatten(self):
        """
        Генерация плоского списка из параметров вакансии
        """
        flat_vacancy = list()
        flat_vacancy.append(self.id)
        flat_vacancy.append(self.name)
        flat_vacancy.append(self.url)
        flat_vacancy.append(self.description)
        flat_vacancy.append(self.experience)
        flat_vacancy.append(self.key_skills)
        flat_vacancy.append(self.short)
        flat_vacancy.append(self.cteated_at)
        flat_vacancy.append(self.published_at)
        flat_vacancy.append(self.edited_at)
        flat_vacancy.append(self.salary_from)
        flat_vacancy.append(self.salary_to)
        flat_vacancy.append(self.avg_salary)
        flat_vacancy.append(self.str_salary)
        flat_vacancy.append(self.city)
        flat_vacancy.append(self.street)
        flat_vacancy.append(self.employer_id)
        flat_vacancy.append(self.employer_name)
        flat_vacancy.append(self.employer_url)
        flat_vacancy.append(self.employer_logo)
        return flat_vacancy


class VacancyManager:
    """
    Класс-обработчик для Vacancy
    Организует взаимодействие остальной программы с классом вакансий
    """
    def __init__(self, name, raw_vacancies):
        """
        Генерация множества экземпляров вакансии из json-словаря
        """
        self.name = name
        self._memory = {}
        duplicates = 0
        for raw_vacancy in raw_vacancies:
            duplicates += self.add_vacancy(raw_vacancy)

        text = f'Инициация "{self.name}", {len(raw_vacancies)} вакансий ({duplicates} повт.)'
        responds.save(text, level=3)
        Overlord.add_manager(self)

    def __add__(self, other):
        """
        Суммирование менеджеров с объединением вакансий
        """
        name = self.name + '+' + other.name
        source = list({**self.unfold(), **other.unfold()})
        new_manager = VacancyManager(name=name, raw_vacancies=source)
        return new_manager

    def unfold(self):
        """
        Выдать содержимое памяти
        """
        return self._memory

    def add_vacancy(self, raw_vacancy):
        """
        Генерация нового экземпляра вакансии из json-словаря
        """
        current_id = int(raw_vacancy.get('id'))
        if current_id not in self._memory:
            self._memory[current_id] = Vacancy(raw_vacancy)
            return 0
        return 1

    def del_vacancy(self, target_id):
        """
        Удаление вакансии
        """
        success = self._memory.pop(target_id, False)
        if not success:
            text = f'Попытка удалить несуществующую вакансию {target_id} у менеджера "{self.name}""'
            responds.save(text, level=3)

    def has_vacancy(self, target_id):
        """
        Проверка наличия вакансии
        """
        if target_id in self._memory:
            return True
        return False

    def get_vacancy(self, target_id):
        """
        Получение вакансии
        """
        if VacancyManager.has_vacancy(self, target_id):
            return self._memory[target_id]
        else:
            txt = f'Попытка запросить несуществующую вакансию {target_id} у менеджера "{self.name}"'
            responds.save(txt, level=3)

    def demonstrate(self):
        """
        Вывод всех вакансий на экран
        """
        total = len(self._memory)
        digits = len(str(total))
        responds.save(f'Вывод вакансий "{self.name}" на экран в кол-ве {total} шт.', level=2)
        print(f'В памяти находится {total} записей:')
        for i, each in enumerate(self._memory, start=1):
            num = str(i).rjust(digits, '0')
            print(f'\t{num}. {each}')

    def erase_memory(self):
        """
        Полная очистка памяти менеджера
        """
        responds.save(f'Очистка памяти "{self.name}" в количестве {len(self._memory)} шт.', level=3)
        self._memory.clear()

    def detail_vacancy(self, vacancy_id):
        """
        Запросить подробности вакансии
        """
        raw_details = hh_api.load_vacancy_detailed(vacancy_id)
        self._memory[vacancy_id].info = handlers.handle_info(raw_details)

    def detail_all(self):
        """
        Запросить подробности всех вакансий
        """
        for vacancy in self._memory.keys():
            self.detail_vacancy(vacancy)

    def purge_with_words(self, words):
        """
        Удалить все вакансии, в описании которых есть данные слова
        """
        text = f'Удаление по наличию ключевых слов "{words}" менеджера "{self.name}"'
        responds.save(text, level=2)
        for word in words:
            for each in self._memory.values():
                if each.info.description is not None and word in each.info.description:
                    self.del_vacancy(each.id)

                if each.info.short is not None and word in each.info.short:
                    self.del_vacancy(each.id)

    def purge_without_words(self, words):
        """
        Удалить все вакансии, в описании которых нет данных слов
        """
        text = f'Удаление по отсутствию ключевых слов "{words}" менеджера "{self.name}"'
        responds.save(text, level=2)
        for word in words:
            for each in self._memory.values():
                if each.info.description is not None and word in each.info.description:
                    self.del_vacancy(each.id)

                if each.info.short is not None and word in each.info.short:
                    self.del_vacancy(each.id)

    def total(self):
        responds.save(f'Общее количество вакансий в выборке: {len(self._memory)}', level=2)

    def generate_short_html(self):
        """
        Генерация упрощённого HTML списка
        """
        html = hh_html.short_html(self._memory)

        with open('output.html', mode='w', encoding='utf-8') as file:
            for line in html:
                file.write(line)
