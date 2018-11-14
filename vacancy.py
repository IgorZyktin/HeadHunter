# -*- coding: utf-8 -*-
"""

    В этом модуле находится класс вакансии и его управляющий класс

"""
import handlers
import resp
import hh_html
import json


class Vacancy:
    """
    Главный класс всех вакансий.
    Выступает основным хранилищем данных
    """
    def __init__(self, raw_data):
        self.id = int(raw_data.get('id'))
        self.url = raw_data.get('alternate_url')
        self.name = raw_data.get('name')

        self.raw_data = json.dumps(raw_data, ensure_ascii=False)

        self.info = handlers.handle_info(raw_data)
        self.date = handlers.handle_date(raw_data)
        self.salary = handlers.handle_salary(raw_data)
        self.location = handlers.handle_location(raw_data)
        self.employer = handlers.handle_employer(raw_data)

    def __str__(self):
        return f'{self.id} {self.salary.str_salary} {self.name}'

    def __repr__(self):
        return '[VAC] ' + str(self.id)


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
        resp.save(text, level=3)

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
            resp.save(text, level=3)

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
            resp.save(txt, level=3)

    def demonstrate(self):
        """
        Вывод всех вакансий на экран
        """
        total = len(self._memory)
        digits = len(str(total))
        resp.save(f'Вывод вакансий "{self.name}" на экран в кол-ве {total} шт.', level=2)
        print(f'В памяти находится {total} записей:')
        for i, each in enumerate(self._memory, start=1):
            num = str(i).rjust(digits, '0')
            print(f'\t{num}. {each}')

    def erase_memory(self):
        """
        Полная очистка памяти менеджера
        """
        resp.save(f'Очистка памяти "{self.name}" в количестве {len(self._memory)} шт.', level=3)
        self._memory.clear()

    def purge_with_words(self, words):
        """
        Удалить все вакансии, в описании которых есть данные слова
        """
        text = f'Удаление по наличию ключевых слов "{words}" менеджера "{self.name}"'
        resp.save(text, level=2)
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
        resp.save(text, level=2)
        for word in words:
            for each in self._memory.values():
                if each.info.description is not None and word in each.info.description:
                    self.del_vacancy(each.id)

                if each.info.short is not None and word in each.info.short:
                    self.del_vacancy(each.id)

    def total(self):
        resp.save(f'Общее количество вакансий в выборке: {len(self._memory)}', level=2)

    def generate_short_html(self):
        """
        Генерация упрощённого HTML списка
        """
        html = hh_html.short_html(self._memory)

        with open('output.html', mode='w', encoding='utf-8') as file:
            for line in html:
                file.write(line)
