# -*- coding: utf-8 -*-
"""

    Модуль обработки HTML

"""
import operator


def short_html(vacancies):
    """
    Генерация файла с короткими описаниями вакансий
    """
    html = list()

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
    <h1>Вакансий в списке: {0}</h1>
    </div>
    """.format(len(vacancies))

    html.extend(header1)
    html.extend(header2)

    for vacancy in sorted(vacancies.values(), key=operator.attrgetter('attr_06_salary_avg_')):

        if vacancy.attr_10_description:
            text = vacancy.attr_10_description
        else:
            text = vacancy.attr_11_short_descr

        vac_id = vacancy.attr_01_id__
        url = vacancy.attr_03_url_
        name = vacancy.attr_02_name
        salary = vacancy.attr_07_salary_str_

        info = """ 
        <div class="vacancy_short">
        <button class="button button1" onclick="openbox({0}); return false">Подробности</button>
        <b>{0}</b>: {3} <a href="{1}">{2}</a>
        <div id="{0}" style="display:none;" class="descr">
        {4}
        <br>
        </div></div>
        """.format(vac_id, url, name, salary, text)
        html.extend(info)
    html.append('</body>\n')
    html.append('</html>\n')
    return html
