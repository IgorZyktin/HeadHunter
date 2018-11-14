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
    VacancyManager.initiate(raw_data)
    VacancyManager.total()
    #VacancyManager.purge_with_words('C++', 'responsibility')
    #VacancyManager.purge_with_words('C++', 'requirement')
    #VacancyManager.show_all()
    #va = hh_api.load_vacancy(28427634)
    VacancyManager.generate_short_html()

if __name__ == '__main__':
    main()
