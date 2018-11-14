# -*- coding: utf-8 -*-
"""

    Основной модуль программы

"""
import hh_api
from vacancy import VacancyManager


def main():
    """
        Главная функция
    """
    raw_data = hh_api.get_data(keyword='python', area=1)
    initial_manager = VacancyManager('initial', raw_data)
    initial_manager.total()
    #VacancyManager.purge_with_words('C++', 'responsibility')
    #VacancyManager.purge_with_words('C++', 'requirement')
    #VacancyManager.show_all()
    #va = hh_api.load_vacancy_detailed(28427634)
    initial_manager.generate_short_html()


if __name__ == '__main__':
    main()
