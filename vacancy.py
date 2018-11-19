# -*- coding: utf-8 -*-
"""

    В этом модуле находится класс вакансии и его управляющий класс

"""
import handlers
import hh_api
import responds
import hh_html


class Overlord:
    """
    Сборщик данных по созданным экземплярам
    """
    _managers = {}

    @staticmethod
    def add_manager(name, manager):
        Overlord._managers.update({name: manager})

    @staticmethod
    def enlist_managers():
        for name, manager in Overlord._managers.items():
            print(name, manager.total())

    @staticmethod
    def delete_manager(name):
        del Overlord._managers[name]


class Vacancy:
    """
    Базовый класс вакансии
    """
    __slots__ = ['attr_01_id__',
                 'attr_02_name',
                 'attr_03_url_',
                 'attr_04_salary_from',
                 'attr_05_salary_upto',
                 'attr_06_salary_avg_',
                 'attr_07_salary_str_',
                 'attr_08_experience_',
                 'attr_09_key_skills_',
                 'attr_10_description',
                 'attr_11_short_descr',
                 'attr_12_employer_id__',
                 'attr_13_employer_url_',
                 'attr_14_employer_name',
                 'attr_15_time_created',
                 'attr_16_time_publish',
                 'attr_17_time_dbsaved',
                 'attr_18_addr_city__',
                 'attr_19_addr_street']

    def __init__(self, raw_data):
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
        return f'{self.attr_01_id__} {self.attr_07_salary_str_} {self.attr_02_name}'

    def __repr__(self):
        return '[VAC] ' + str(self.attr_01_id__)

    @staticmethod
    def attribute_names():
        """
        Выдать перечень атрибутов
        """
        return Vacancy.__slots__

    def attribute_values(self):
        """
        Выдать значения атрибутов
        """
        values = []
        for attr_name in self.__slots__:
            values.append(getattr(self, attr_name))
        return values


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
        Overlord.add_manager(name, self)

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
        if not raw_vacancy:
            text = f'Попытка создать вакансию из ошибочных данных: {raw_vacancy} у менеджера "{self.name}""'
            responds.save(text, level=3)

        raw_id = raw_vacancy.get('id')

        if raw_id is None:
            text = f'Отсутствие поля "id" в исходных данных: {raw_vacancy} у менеджера "{self.name}""'
            responds.save(text, level=3)
        else:
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
        self.del_vacancy(vacancy_id)
        self.add_vacancy(raw_details)

    def detail_all(self):
        """
        Запросить подробности всех вакансий
        """
        for vacancy in self._memory.keys():
            self.detail_vacancy(vacancy)

    def purge_with(self, words, fields=('attr_10_description', 'attr_11_short_descr')):
        """
        Удалить все вакансии, в описании которых есть данные слова
        """
        total = 0
        for word in words:
            for each in list(self._memory.values()):
                for field in fields:
                    found = getattr(each, field)
                    if found:
                        if word in found:
                            self.del_vacancy(each.attr_01_id__)
                            total += 1

            responds.save(f'Удал. {total} вак. по наличию ключевого слова "{word}" в менеджере "{self.name}"', level=2)
        responds.save(f'Вакансий в менеджере "{self.name}" после удаления: {self.total()}', level=2)

    def purge_without(self, words, fields=('attr_10_description', 'attr_11_short_descr')):
        """
        Удалить все вакансии, в описании которых нет данных слов
        """
        text = f'Удаление по отсутствию ключевых слов "{words}" менеджера "{self.name}"'
        responds.save(text, level=2)
        total = 0
        for word in words:
            for each in list(self._memory.values()):
                for field in fields:
                    found = getattr(each, field)
                    if found:
                        if word not in found:
                            self.del_vacancy(each.attr_01_id__)
                            total += 1
            responds.save(f'Удал. {total} вак. по отсутствию ключевого слова "{word}" в менеджере "{self.name}"', level=2)
        responds.save(f'Вакансий в менеджере "{self.name}" после удаления: {self.total()}', level=2)

    def purge_by_field(self, status, field='attr_10_description'):
        """
        Удалить все вакансии, в описании которых есть/нет указанного поля
        """
        total = 0
        for each in list(self._memory.values()):
            found = getattr(each, field)
            if bool(found) == status:
                self.del_vacancy(each.attr_01_id__)
                total += 1

        present = ['наличию', 'отстутствию'][status]
        text = f'Удаление {total} вакансий по {present} ключевого поля "{field}" в менеджере "{self.name}"'
        responds.save(text, level=2)
        if total:
            responds.save(f'Вакансий в менеджере "{self.name}" после удаления: {self.total()}', level=2)

    def total(self):
        """
        Вернуть суммарное число вакансий в данном менеджере
        """
        return len(self._memory)

    def generate_html(self):
        """
        Генерация упрощённого HTML списка
        """
        html = hh_html.short_html(self._memory)

        with open('output.html', mode='w', encoding='utf-8') as file:
            for line in html:
                file.write(line)
