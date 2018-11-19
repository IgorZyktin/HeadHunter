# -*- coding: utf-8 -*-
"""

    Модуль настройки обратной связи

"""
import logging
from colorama import init, Fore
init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    filename='headhunter.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

LEVEL = 1


def save(text, color=None, level: int = 1):
    """
    Вывод всех данных скрипта собран в этой функции
    """
    if level == 1:
        # 1 - Самое подробное описание
        resulting_color = Fore.GREEN
        logging.info(text)

    elif level == 2:
        # 2 - Незначительные события
        resulting_color = Fore.LIGHTGREEN_EX
        logging.info(text)

    elif level == 3:
        # 3 - Важные события
        resulting_color = Fore.YELLOW
        logging.warning(text)

    elif level == 4:
        # 4 - Очень важные события
        resulting_color = Fore.LIGHTRED_EX
        logging.error(text)

    elif level == 5:
        # 5 - Критический сбой
        resulting_color = Fore.RED
        logging.critical(text)

    else:
        resulting_color = Fore.WHITE

    if color is not None:
        resulting_color = color

    if level >= LEVEL:
        print(resulting_color + text)
