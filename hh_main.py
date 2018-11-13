import hh_api
from hh_vacancy import VacancyManager

raw_data = hh_api.retrieve_vacancies('', local=True)
VacancyManager.initiate(raw_data)
VacancyManager.show_all()
