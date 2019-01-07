# -*- coding: utf-8 -*-
"""

    В этом модуле находится класс вакансии и его управляющий класс

"""
import handlers
import internet
import html


class Vacancy:
    """
    Базовый класс вакансии
    """
    def __init__(self, raw_data):
        # генерация из JSON
        self.attr_01_id__ = int(raw_data.get('id'))
        self.attr_02_name = raw_data.get('name')
        self.attr_03_url_ = raw_data.get('alternate_url')

        salary = handlers.handle_salary(raw_data)
        self.attr_04_salary_from = salary.attr_04_salary_from
        self.attr_05_salary_upto = salary.attr_05_salary_upto
        self.attr_06_salary_avg_ = salary.attr_06_salary_avg_
        self.attr_07_salary_str_ = salary.attr_07_salary_str_

        description = handlers.handle_info(raw_data)
        self.attr_08_experience_ = description.attr_08_experience_
        self.attr_09_key_skills_ = description.attr_09_key_skills_
        self.attr_10_description = description.attr_10_description
        self.attr_11_short_descr = description.attr_11_short_descr

        employer = handlers.handle_employer(raw_data)
        self.attr_12_employer_id__ = employer.attr_12_employer_id__
        self.attr_13_employer_url_ = employer.attr_13_employer_url_
        self.attr_14_employer_name = employer.attr_14_employer_name

        date = handlers.handle_time(raw_data)
        self.attr_15_time_created = date.attr_15_time_created
        self.attr_16_time_publish = date.attr_16_time_publish
        self.attr_17_time_dbsaved = date.attr_17_time_dbsaved

        address = handlers.handle_location(raw_data)
        self.attr_18_addr_city__ = address.attr_18_addr_city__
        self.attr_19_addr_street = address.attr_19_addr_street

    def __str__(self):
        return f'[{self.attr_01_id__}] {self.attr_07_salary_str_} {self.attr_02_name}'

    def __repr__(self):
        return f'[{self.attr_01_id__}] {self.attr_07_salary_str_} {self.attr_02_name}'


class VacancyManager:
    """
    Класс-обработчик для Vacancy
    """
    def __init__(self, keyword, area):
        """
        Создание пустого менеджера
        """
        self.keyword = keyword
        self._memory = {}
        raw_vacancies = internet.load_vacancies(keyword, area)
        for raw_vacancy in raw_vacancies:
            self.add_one(raw_vacancy)

    def add_one(self, raw_vacancy):
        """
        Генерация нового экземпляра вакансии
        """
        if isinstance(raw_vacancy, list):
            current_id = raw_vacancy[0]
        else:
            current_id = raw_vacancy.get('id')

        try:
            current_id = int(current_id)
            if current_id not in self._memory:
                self._memory[current_id] = Vacancy(raw_vacancy)
        except TypeError:
            print('Ошибка для вакансии', current_id)

    def get_memory(self):
        """
        Выдать содержимое памяти
        """
        return self._memory

    def del_vacancy(self, target_id):
        """
        Удаление вакансии
        """
        self._memory.pop(target_id)

    def demonstrate(self):
        """
        Вывод всех вакансий на экран
        """
        total = len(self._memory)
        digits = len(str(total))
        print(f'\tВ памяти находится {total} записей:')
        for i, each in enumerate(self._memory.values(), start=1):
            num = str(i).rjust(digits, '0')
            print(f'\t\t{num}. {each}')

    def erase_memory(self):
        """
        Полная очистка памяти менеджера
        """
        self._memory.clear()

    def detail_vacancy(self, vacancy_id):
        """
        Запросить подробности вакансии
        """
        raw_detailed = internet.load_detailed(vacancy_id)
        Vacancy.__init__(self._memory[vacancy_id], raw_detailed)

    def detail_all(self):
        """
        Запросить подробности всех вакансий
        """
        print()
        for i, vacancy in enumerate(self._memory.keys(), start=1):
            print(f'\r\tЗапрос на детализацию, вакансия {i} из {len(self._memory)}', end='')
            self.detail_vacancy(vacancy)
        print(f'\r\t{i} шт. вакансий успешно обработано')
        print()

    def purge_with(self, words):
        """
        Удалить все вакансии, в описании которых есть данные слова
        """
        fields = ['attr_08_experience_', 'attr_09_key_skills_',
                  'attr_10_description', 'attr_11_short_descr']
        total = 0
        for word in words:
            for each in list(self._memory.values()):
                for field in fields:
                    found = getattr(each, field)
                    if found:
                        if word in found:
                            self.del_vacancy(each.attr_01_id__)
                            total += 1

            print(f'\tУдалено {total} вакансий по наличию ключевого слова "{word}"'
                  + f' (осталось {self.total()})')

    def purge_without(self, words: list):
        """
        Удалить все вакансии, в описании которых нет данных слов
        """
        fields = ['attr_08_experience_', 'attr_09_key_skills_',
                  'attr_10_description', 'attr_11_short_descr']
        total = 0
        for word in words:
            for each in list(self._memory.values()):
                for field in fields:
                    found = getattr(each, field)
                    if found:
                        if word not in found:
                            self.del_vacancy(each.attr_01_id__)
                            total += 1
            print(f'\tУдалено {total} вакансий по отсутствию ключевого слова "{word}"'
                  + f' (осталось {self.total()})')

    def total(self):
        """
        Вернуть суммарное число вакансий в данном менеджере
        """
        return len(self._memory)

    def generate_html(self):
        """
        Генерация HTML вывода
        """
        name = self.keyword + '.html'
        html_document = html.generate_html(self._memory)

        with open(name, mode='w', encoding='utf-8') as file:
            for line in html_document:
                file.write(line)
