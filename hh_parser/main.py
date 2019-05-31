# -*- coding: utf-8 -*-
"""

    Основной модуль программы

"""
from colorama import Fore, init

from hh_handlers import tokenize, is_int
from hh_vacancy import VacancyManager
init(autoreset=True)


def greetings():
    """
    Вывод стартового текста
    """
    print()
    print(Fore.LIGHTBLUE_EX + ' HeadHunter '.center(79, '~'))
    print(Fore.LIGHTBLUE_EX + ' Поисковый робот '.center(79, '~'))
    print()
    print('\tПримеры запросов:')
    print('\t' + Fore.YELLOW + '> Сварщик')
    print('\t' + Fore.YELLOW + '> Сварщик, Тверь')
    print('\t' + Fore.YELLOW + '> Сварщик AND аргон, Тверь')
    print('\t' + Fore.YELLOW + '> Сварщик and аргон not мангал, Тверь')
    print('\t' + Fore.YELLOW + '> Сварщик AND аргон NOT мангал, Тверь')


def main():
    """
    Главная функция
    """
    greetings()
    while True:
        print()
        print('\tВведите поисковый запрос:')

        user_input = input('\t> ')
        # user_input = 'Сварщик AND аргон NOT мангал, Тверь'

        if not user_input:
            continue

        print('\tПолучено:', Fore.LIGHTRED_EX + user_input)
        print()

        request, with_this, without_this, city_name, city_code = tokenize(user_input)

        print('\tОсновной запрос:', Fore.YELLOW + request)

        if with_this:
            print('\t    Должно быть:', Fore.BLUE + ', '.join(with_this))

        if without_this:
            print('\t Не должно быть:', Fore.RED + ', '.join(without_this))

        print('\t В каком городе:', city_name.title(), f'(код {city_code})')

        print()
        print('\tЗапрос распознан правильно? 1 - да, 0 - нет')

        user_agreement = input('\t> ')

        print()
        if not is_int(user_agreement):
            continue

        if int(user_agreement) == 0:
            continue

        print('\tОтправляем запрос на сервер hh.ru...')
        manager = VacancyManager(keyword=user_input, area=city_code)

        if with_this:
            manager.purge_without(with_this)

        if without_this:
            manager.purge_with(without_this)

        manager.demonstrate()
        if manager.total() == 0:
            continue

        print('\tЗапросить подробности по найденным вакансиям? 1 - да, 0 - нет')
        user_agreement = input('\t> ')
        print()

        if not is_int(user_agreement):
            continue

        if int(user_agreement) == 0:
            continue

        manager.detail_all()
        manager.generate_results()
        manager.erase_memory()
        del manager


if __name__ == '__main__':
    main()
