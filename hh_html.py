# -*- coding: utf-8 -*-
"""

    Модуль обработки HTML

"""
import operator


def short_html(vacancies):
    """
    Генерация файла с корткими описаниями вакансий
    """
    html = list()
    header = """
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

    html.extend(header)
    html.extend(header2)

    for vacancy in sorted(vacancies.values(), key=operator.attrgetter('salary.avg_salary')):
        if vacancy.info.description:
            text = vacancy.info.description
        else:
            text = vacancy.info.short

        salary = vacancy.salary.str_salary

        info = f""" 
        <div class="vacancy_short">
        <button class="button button1" onclick="openbox({vacancy.id}); return false">Подробности</button>
        <b>{vacancy.id}</b>: {salary} <a href="{vacancy.url}">{vacancy.name}</a>
        <div id="{vacancy.id}" style="display:none;" class="descr">
        {text}
        <br>
        </div></div>
        """
        html.extend(info)
    html.append('</body>\n')
    html.append('</html>\n')
    return html
