# -*- coding: utf-8 -*-
"""

    Основной модуль программы

"""
import hh_api
import database
from vacancy import VacancyManager


def main():
    """
        Главная функция
    """
    raw_data = hh_api.get_data(keyword='python', area=1)
    initial_manager = VacancyManager('initial', raw_data)
    initial_manager.purge_with(['C++', 'devops'])
    initial_manager.purge_by_field(False, 'attr_06_salary_avg_')
    #VacancyManager.show_all()
    #database.dump(initial_manager.unfold())
    initial_manager.detail_vacancy(28796180)
    initial_manager.detail_vacancy(28514412)
    #initial_manager.detail_all()
    initial_manager.generate_html()
    #database.drop_db()


if __name__ == '__main__':
    main()
