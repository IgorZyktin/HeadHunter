"""

    В этом модуле находится класс вакансии и его обработчик

"""
import operator
import handlers
import resp
import hh_html


class Vacancy:
    """
    Главный класс всех вакансий.
    Выступает основным хранилищем данных
    """
    def __init__(self, raw_data):
        self.id = int(raw_data.get('id'))
        self.url = raw_data.get('alternate_url')
        self.name = raw_data.get('name')

        self.source = raw_data

        self._date = handlers.HandleDate(raw_data)
        self._salary = handlers.HandleSalary(raw_data)
        self._location = handlers.HandlerLocation(raw_data)
        self._employer = handlers.HandleEmployer(raw_data)
        self._snippets = handlers.HandleSnippets(raw_data)

    def __str__(self):
        return f'{self.id} {self.salary} {self.name}'

    def __repr__(self):
        return '[VAC] ' + str(self.id)

    @property
    def salary(self):
        return self._salary.salary

    @property
    def avg_salary(self):
        return self._salary.avg_salary

    @property
    def responsibility(self):
        return self._snippets.responsibility

    @property
    def requirement(self):
        return self._snippets.requirement

    @property
    def date(self):
        return self._date.date

    @property
    def employer(self):
        return self._employer.employer

    @property
    def location(self):
        return self._location.metro


class VacancyManager:
    """
    Класс-обработчик для Vacancy.
    Организует взаимодействие остальной программы с классом вакансий
    """
    memory = []
    actual_ids = {}

    @staticmethod
    def initiate(raw_data):
        # генерация новых экземпляров вакансий из списка json-словарей
        dupl = 0
        for raw_vacancy in raw_data:
            if int(raw_vacancy.get('id')) in VacancyManager.actual_ids:
                dupl += 1
            else:
                VacancyManager.add_vacancy(raw_vacancy)
        VacancyManager.memory.sort(key=operator.attrgetter('avg_salary'))
        resp.save(f'Генерация вакансий, {len(raw_data)} шт. ({dupl} повт.)', level=3)

    @staticmethod
    def add_vacancy(raw_vacancy):
        # генерация одного нового экземпляра вакансии из json-словаря
        if int(raw_vacancy.get('id')) not in VacancyManager.actual_ids:
            new_vacancy = Vacancy(raw_vacancy)
            VacancyManager.actual_ids.update({new_vacancy.id: new_vacancy})
            VacancyManager.memory.append(new_vacancy)

    @staticmethod
    def del_vacancy_by_id(vacancy_id):
        # удаление вакансии
        VacancyManager.memory.remove(VacancyManager.actual_ids[vacancy_id])
        del VacancyManager.actual_ids[vacancy_id]

    @staticmethod
    def get_vacancy_by_index(number):
        # получение вакансии из списка существующщих вакансий по индексу
        if 0 <= number <= len(VacancyManager.memory):
            return VacancyManager.memory[number]
        raise IndexError(f'Нет вакансии с таким индексом: {number}')

    @staticmethod
    def get_vacancy_by_id(number):
        # получение вакансии из списка существующщих вакансий по id
        if number in VacancyManager.actual_ids:
            return VacancyManager.actual_ids[number]
        raise IndexError(f'Нет вакансии с таким id: {number}')

    @staticmethod
    def show_all():
        total = len(VacancyManager.memory)
        digits = len(str(total))
        resp.save(f'Вывод вакансий на экран {total}', level=2)
        print(f'В памяти находится {total} записей:')
        for i, each in enumerate(VacancyManager.memory, start=1):
            num = str(i).rjust(digits, '0')
            print(f'\t{num}. {each}')

    @staticmethod
    def clear():
        resp.save(f'Очистка списка вакансий {len(VacancyManager.memory)}', level=3)
        for i in range(len(VacancyManager.memory)):
            del VacancyManager.memory[0]
        VacancyManager.memory.clear()
        VacancyManager.actual_ids.clear()

    @staticmethod
    def purge_with_words(words, field):
        resp.save(f'Удаление вакансий с ключевыми словами "{words}" в поле "{field}" ', level=3)
        for word in words:
            if field == 'requirement':
                for each in VacancyManager.memory:
                    if each.requirement.find(word) != -1:
                        VacancyManager.del_vacancy_by_id(each.id)

            elif field == 'responsibility':
                for each in VacancyManager.memory:
                    if each.responsibility.find(word) != -1:
                        VacancyManager.del_vacancy_by_id(each.id)

    @staticmethod
    def purge_without_words(words, field):
        resp.save(f'Удаление вакансий без ключевых слов: {words} - {field} ', level=3)
        for word in words:
            if field == 'requirement':
                for each in VacancyManager.memory:
                    if each.requirement.find(word) == -1:
                        VacancyManager.del_vacancy_by_id(each.id)

            elif field == 'responsibility':
                for each in VacancyManager.memory:
                    if each.responsibility.find(word) == -1:
                        VacancyManager.del_vacancy_by_id(each.id)

    @staticmethod
    def total():
        resp.save(f'Общее количество вакансий в выборке: {len(VacancyManager.memory)}', level=2)

    @staticmethod
    def generate_short_html():
        html = hh_html.short_html(VacancyManager.memory)

        with open('output.html', mode='w', encoding='utf-8') as file:
            for line in html:
                file.write(line)
