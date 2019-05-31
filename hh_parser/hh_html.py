# -*- coding: utf-8 -*-
"""

    Модуль обработки HTML

"""
import operator
from colorama import Fore, init
init(autoreset=True)


def generate_html(keyword: str, vacancies: dict) -> list:
    """
    Генерация файла с короткими описаниями вакансий
    """
    header1 = """
<!DOCTYPE html>
<html>
<style>
.vacancy_short {
    font-size:18px;
    border-radius: 10px;
    width: 60%;
    margin: 1%;
    padding: 0.5%;
    margin-left: auto;
    margin-right: auto;
    box-shadow: 0 3px 16px 2px rgba(0, 0, 0, 0.48);
    text-align: justify;
    background-color: white;
}

.header {
    font-size:18px;
    border-radius: 10px;
    width: 60%;
    margin: 1%;
    padding: 0.5%;
    margin-left: auto;
    margin-right: auto;
    box-shadow: 0 3px 16px 2px rgba(0, 0, 0, 0.48);
    text-align: center;
    background-color: white;
}

.descr {
    font-size:18px;
    border-radius: 10px;
    width: 98%;
    padding: 1%;
    margin-top: 20px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: auto;
    box-shadow: 0 3px 16px 2px rgba(0, 0, 0, 0.48);
    text-align: justify;
    background-color: #c2d6eb;
}

td {
    text-align: center;
}

body {
    margin-right: 10%;
    margin-left: 10%;
    background-color: gray;
    font-family: 'Istok Web', sans-serif;
}

.button {
    position: relative;
    background-color: #555555;
    border-radius: 2px;
    border: none;
    color: white;
    padding: 6px 30px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 5px 1%;
    -webkit-transition-duration: 0.4s; /* Safari */
    transition-duration: 0.4s;
    cursor: pointer;
}

.button1 {
    background-color: white;
    color: black;
    border: 2px solid #032c58;
}

.button1:hover {
    background-color: #032c58;
    color: white;
}
</style>
<script type="text/javascript">
function openbox(id){
    display = document.getElementById(id).style.display;

    if(display=='none'){
       document.getElementById(id).style.display='block';
    }else{
       document.getElementById(id).style.display='none';
    }
}
</script>
<body>
    """

    header2 = """
<div class="header">
<h1><b>{0}</b></h1>
<h2>Вакансий в списке: {1}</h2>
</div>
    """.format(keyword, len(vacancies))

    html = list()
    html.extend(header1)
    html.extend(header2)

    for vacancy in sorted(vacancies.values(),
                          key=operator.attrgetter('attr_06_salary_avg_')):
        if vacancy.attr_10_description:
            text = vacancy.attr_10_description
        else:
            text = vacancy.attr_11_short_descr

        experience = vacancy.attr_08_experience_
        vac_id = vacancy.attr_01_id__
        url = vacancy.attr_03_url_
        name = vacancy.attr_02_name
        salary = vacancy.attr_07_salary_str_

        info = """
<div class="vacancy_short">
    <table border=0 width="100%">
    <tr>
    <td width="15%"><button class="button button1" onclick="openbox({id}); return false">Подробности</button></td>
    <td width="10%"><b>{id}</b></td>
    <td width="15%">{exp}</td>
    <td width="15%">{salary}</td>
    <td style="text-align:left"><a href="{url}">{name}</a></td>
    </tr>
    </table>
    <div id="{id}" style="display:none;" class="descr">
    {text}
    </div>
</div>
        """.format(id=vac_id, url=url, name=name, salary=salary, text=text, exp=experience)
        html.extend(info)
    html.append('</body>\n')
    html.append('</html>\n')
    return html


def save_html(keyword: str, path: str, data: dict) -> bool:
    """
        Сохранение результатов в HTML
    """
    if not keyword or not path or not data:
        return False

    html_document = generate_html(keyword, data)

    try:
        with open(path, mode='w', encoding='utf-8') as file:
            for line in html_document:
                file.write(line)
        return True

    except PermissionError:
        print()
        print(Fore.RED + '\tНевозможно перезаписать файл:')
        print('\t', Fore.RED + path)
        print(Fore.RED + '\tВозможно документ открыт в другой программе.')
        print()

    except OSError:
        print()
        print(Fore.RED + '\tНевозможно сохранить файл:')
        print('\t', Fore.RED + path)
        print()

    return False
