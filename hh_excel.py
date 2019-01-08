"""

    Модуль конвертирования для XLS документов

"""
import re
import xlwt
from colorama import Fore, init
init(autoreset=True)


def remove_tags(input_text: str) -> str:
    """
        Удаление HTML тегов из текста
    """
    html_pattern = r'<.*?>'
    result = re.sub(html_pattern, '', input_text)
    return result


def save_xls(path: str, data: dict):
    """
        Сохранения XLS файла
    """
    if not data or not path:
        return

    book = xlwt.Workbook()
    sheet = book.add_sheet('HH Result')

    sheet.write(0, 0, 'Id')
    sheet.write(0, 1, 'Название вакансии')
    sheet.write(0, 2, 'Ссылка на hh.ru')
    sheet.write(0, 3, 'ЗП от, руб.')
    sheet.write(0, 4, 'ЗП до, руб.')
    sheet.write(0, 5, 'Ср. ЗП, руб.')
    sheet.write(0, 6, 'ЗП, текст')
    sheet.write(0, 7, 'Опыт')
    sheet.write(0, 8, 'Ключевые навыки')
    sheet.write(0, 9, 'Описание вакансии')
    sheet.write(0, 10, 'Id работодателя')
    sheet.write(0, 11, 'URL работодателя')
    sheet.write(0, 12, 'Название компании')
    sheet.write(0, 13, 'Вакансия создана')
    sheet.write(0, 14, 'Вакансия опубликована')
    sheet.write(0, 15, 'Вакансия обработана')
    sheet.write(0, 16, 'Город')
    sheet.write(0, 17, 'Адрес')

    sheet.col(0).width = 10 * 367
    sheet.col(1).width = 15 * 367
    sheet.col(2).width = 15 * 367
    sheet.col(3).width = 8 * 367
    sheet.col(4).width = 8 * 367
    sheet.col(5).width = 8 * 367
    sheet.col(6).width = 8 * 367
    sheet.col(7).width = 12 * 367
    sheet.col(8).width = 12 * 367
    sheet.col(9).width = 25 * 367
    sheet.col(10).width = 8 * 367
    sheet.col(11).width = 18 * 367
    sheet.col(12).width = 18 * 367
    sheet.col(13).width = 12 * 367
    sheet.col(14).width = 12 * 367
    sheet.col(15).width = 12 * 367
    sheet.col(16).width = 12 * 367
    sheet.col(17).width = 20 * 367

    for i, vacancy in enumerate(data.values(), start=1):
        sheet.write(i, 0, vacancy.attr_01_id__)
        sheet.write(i, 1, vacancy.attr_02_name)
        sheet.write(i, 2, vacancy.attr_03_url_)
        sheet.write(i, 3, vacancy.attr_04_salary_from)
        sheet.write(i, 4, vacancy.attr_05_salary_upto)
        sheet.write(i, 5, vacancy.attr_06_salary_avg_)
        sheet.write(i, 6, vacancy.attr_07_salary_str_)
        sheet.write(i, 7, vacancy.attr_08_experience_)
        sheet.write(i, 8, vacancy.attr_09_key_skills_)

        if vacancy.attr_10_description:
            sheet.write(i, 9, remove_tags(vacancy.attr_10_description))
        else:
            sheet.write(i, 9, remove_tags(vacancy.attr_11_short_descr))

        sheet.write(i, 10, vacancy.attr_12_employer_id__)
        sheet.write(i, 11, vacancy.attr_13_employer_url_)
        sheet.write(i, 12, vacancy.attr_14_employer_name)
        sheet.write(i, 13, vacancy.attr_15_time_created)
        sheet.write(i, 14, vacancy.attr_16_time_publish)
        sheet.write(i, 15, vacancy.attr_17_time_dbsaved)
        sheet.write(i, 16, vacancy.attr_18_addr_city__)
        sheet.write(i, 17, vacancy.attr_19_addr_street)

    try:
        book.save(path)
    except PermissionError:
        print()
        print(Fore.RED + '\tНевозможно перезаписать файл:')
        print('\t', Fore.RED + path)
        print(Fore.RED + '\tВозможно документ открыт в другой программе.')
        print()
        return
    except OSError:
        print()
        print(Fore.RED + '\tНевозможно сохранить файл:')
        print('\t', Fore.RED + path)
        print()
