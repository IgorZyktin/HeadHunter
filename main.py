# -*- coding: utf-8 -*-
"""

    Основной модуль программы

"""
from handlers import tokenize, is_int
from vacancy import VacancyManager
from colorama import Fore, init
init(autoreset=True)


def main():
    """
        Главная функция
    """
    print()
    print(Fore.LIGHTBLUE_EX + ' HeadHunter '.center(79, '~'))
    print(Fore.LIGHTBLUE_EX + 'Поисковый робот'.center(79, ' '))
    print()
    print('\tПримеры запросов:')
    print('\t\t' + Fore.YELLOW + 'Сварщик')
    print('\t\t' + Fore.YELLOW + 'Сварщик,', Fore.LIGHTMAGENTA_EX + 'Тверь')
    print('\t\t' + Fore.YELLOW + 'Сварщик' + Fore.GREEN + ' AND ' + Fore.BLUE + 'нержавейка, '
          + Fore.LIGHTMAGENTA_EX + 'Тверь')
    print('\t\t' + Fore.YELLOW + 'Сварщик' + Fore.GREEN + ' AND ' + Fore.BLUE + 'нержавейка'
          + Fore.RED + ' NOT ' + Fore.BLUE + 'мангалы, ' + Fore.LIGHTMAGENTA_EX + 'Тверь')

    print()
    print('\tВведите поисковый запрос:')
    while True:
        user_input = input('\t>:')
        if not user_input:
            continue

        # user_input = 'Сварщик AND нержавейка NOT мангалы, Тверь'
        print('\tПолучено:', user_input)

        print()

        request, with_this, without_this, city_name, city_code = tokenize(user_input)

        print('\t    Основной запрос:', Fore.YELLOW + request)

        if with_this:
            print('\t    Что должны быть:', Fore.BLUE + ', '.join(with_this))

        if without_this:
            print('\tЧего не должно быть:', Fore.RED + ', '.join(without_this))

        print('\t     В каком городе:', city_name.title(), f'(код {city_code})')

        print()
        print('\tЗапрос распознан правильно? 1 - да, 0 - нет')
        user_input = input('\t>:')
        print()

        if not is_int(user_input):
            continue

        if int(user_input) == 0:
            continue

        manager = VacancyManager(keyword=request, area=1)

        if with_this:
            manager.purge_without(with_this)

        if without_this:
            manager.purge_with(without_this)

        manager.demonstrate()
        manager.generate_html()
        manager.erase_memory()
        del manager

        print()
        print('\tВведите новый поисковый запрос:')


if __name__ == '__main__':
    main()
