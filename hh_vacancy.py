# -*- coding: utf-8 -*-
"""

    В этом модуле находится класс вакансии и его управляющий класс

"""
import os
from colorama import Fore, init

import hh_handlers
import hh_internet
import hh_html
import hh_excel
init(autoreset=True)


class Vacancy:
    """
    Базовый класс вакансии
    """
    def __init__(self, raw_data):
        # генерация из JSON
        self.attr_01_id__ = int(raw_data.get('id'))
        self.attr_02_name = raw_data.get('name')
        self.attr_03_url_ = raw_data.get('alternate_url')

        salary = hh_handlers.handle_salary(raw_data)
        self.attr_04_salary_from = salary.attr_04_salary_from
        self.attr_05_salary_upto = salary.attr_05_salary_upto
        self.attr_06_salary_avg_ = salary.attr_06_salary_avg_
        self.attr_07_salary_str_ = salary.attr_07_salary_str_

        description = hh_handlers.handle_info(raw_data)
        self.attr_08_experience_ = description.attr_08_experience_
        self.attr_09_key_skills_ = description.attr_09_key_skills_
        self.attr_10_description = description.attr_10_description
        self.attr_11_short_descr = description.attr_11_short_descr

        employer = hh_handlers.handle_employer(raw_data)
        self.attr_12_employer_id__ = employer.attr_12_employer_id__
        self.attr_13_employer_url_ = employer.attr_13_employer_url_
        self.attr_14_employer_name = employer.attr_14_employer_name

        date = hh_handlers.handle_time(raw_data)
        self.attr_15_time_created = date.attr_15_time_created
        self.attr_16_time_publish = date.attr_16_time_publish
        self.attr_17_time_dbsaved = date.attr_17_time_dbsaved

        address = hh_handlers.handle_location(raw_data)
        self.attr_18_addr_city__ = address.attr_18_addr_city__
        self.attr_19_addr_street = address.attr_19_addr_street

    def __str__(self):
        vid = self.attr_01_id__
        salary = str(self.attr_07_salary_str_).center(10)
        name = self.attr_02_name
        return f'[{vid}] {salary} {name}'

    def __repr__(self):
        return self.__str__()


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
        raw_vacancies = hh_internet.load_vacancies(keyword, area)
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
        if not total:
            print('\r' + Fore.RED + f'\tБыли забракованы все найденные вакансии.')
            return
        else:
            print('\r' + Fore.GREEN + f'\tНайдено {total} вакансий.')

        digits = len(str(total))
        for i, each in enumerate(self._memory.values(), start=1):
            num = str(i).rjust(digits, '0')

            if total > 10:
                if i == 1:
                    print()
                    print(Fore.LIGHTGREEN_EX + '\tПервые пять:')

                if i in [1, 2, 3, 4, 5]:
                    print(Fore.LIGHTGREEN_EX + f'\t\t{num}. {each}')

                if i == total - 5:
                    print()
                    print(Fore.LIGHTGREEN_EX + '\tПоследние пять:')

                if i in [total-4, total-3, total-2, total-1, total]:
                    print(Fore.LIGHTGREEN_EX + f'\t\t{num}. {each}')
            else:
                print(Fore.LIGHTGREEN_EX + f'\t\t{num}. {each}')

    def erase_memory(self):
        """
        Полная очистка памяти менеджера
        """
        self._memory.clear()

    def detail_all(self):
        """
        Запросить подробности всех вакансий
        """
        total = self.total()

        if not total:
            return

        print('\tЗапрашиваем подробости для {} вакансий...'.format(total), end='')
        for i, each_id in enumerate(self._memory, start=1):
            raw_detailed = hh_internet.load_detailed(each_id)
            Vacancy.__init__(self._memory[each_id], raw_detailed)
            print('\r\tОбработано вакансий: {} из {}'.format(i, total), end='')
        print('\r\t{} вакансий успешно обработано.'.format(total))

    def purge_with(self, words: list):
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
            if total:
                red_word = Fore.RED + word + Fore.RESET
                print(f'\tУдалено {total} вакансий по наличию ключевого слова "{red_word}"'
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
            if total:
                blue_word = Fore.BLUE + word + Fore.RESET
                print(f'\tУдалено {total} вакансий по отсутствию ключевого слова "{blue_word}"'
                      + f' (осталось {self.total()})')

    def total(self):
        """
        Вернуть суммарное число вакансий в данном менеджере
        """
        return len(self._memory)

    def generate_results(self):
        """
        Генерация HTML и XLS вывода
        """
        if not self._memory:
            return

        save_dir = os.path.join(os.getcwd(), 'Результаты')
        if not os.path.exists(save_dir):
            try:
                os.mkdir(save_dir)
            except OSError:
                print('Невозможно создать каталог для сохранения результатов:', save_dir)
                return

        name_html = os.path.join(save_dir, self.keyword + '.html')
        hh_html.save_html(self.keyword, name_html, self._memory)

        name_xls = os.path.join(save_dir, self.keyword + '.xls')
        hh_excel.save_xls(name_xls, self._memory)

        print('\t' + Fore.LIGHTGREEN_EX + 'Результаты поиска сохранены в файлах:')
        print('\t1. {}'.format(name_html))
        print('\t2. {}'.format(name_xls))
