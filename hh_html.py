# -*- coding: utf-8 -*-
"""

    Модуль обработки HTML

"""
import operator


def generate_html(keyword: str, vacancies: dict) -> list:
    """
    Генерация файла с короткими описаниями вакансий
    """
    header1 = """
    <!DOCTYPE html>
    <html>
    <link href="headhunter.css" rel="stylesheet">
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

    for vacancy in sorted(vacancies.values(), key=operator.attrgetter('attr_06_salary_avg_')):
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
        <td width="15%"><button class="button button1" onclick="openbox({id}); return false">
        Подробности</button></td>
        <td width="10%"><b>{id}</b></td>
        <td width="15%">{exp}</td>
        <td width="15%">{salary}</td>
        <td style="text-align:left"><a href="{url}">{name}</a></td></td>
        </tr>
        </table>
        
        <div id="{id}" style="display:none;" class="descr">{text}<br>
        </div></div>
        """.format(id=vac_id, url=url, name=name, salary=salary, text=text, exp=experience)
        html.extend(info)
    html.append('</body>\n')
    html.append('</html>\n')
    return html


def save_html(keyword: str, path: str, data: dict):
    """
        Сохранение результатов в HTML
    """
    html_document = generate_html(keyword, data)
    with open(path, mode='w', encoding='utf-8') as file:
        for line in html_document:
            file.write(line)
