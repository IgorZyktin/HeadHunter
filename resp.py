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
# 1 - Самое подробное описание
# 2 - Незначительные события
# 3 - Важные события
# 4 - Очень важные события
# 5 - Критический сбой


def save(text, color=None, level: int = 1):
    """
    Вывод всех данных скрипта собран в этой функции
    """
    if level == 1:
        resulting_color = Fore.GREEN
        logging.info(text)

    elif level == 2:
        resulting_color = Fore.LIGHTGREEN_EX
        logging.info(text)

    elif level == 3:
        resulting_color = Fore.YELLOW
        logging.warning(text)

    elif level == 4:
        resulting_color = Fore.LIGHTRED_EX
        logging.error(text)

    elif level == 5:
        resulting_color = Fore.RED
        logging.critical(text)

    else:
        resulting_color = Fore.WHITE

    if color is not None:
        resulting_color = color

    if level >= LEVEL:
        print(resulting_color + text)
