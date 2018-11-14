"""

    Модуль обработчиков

"""
import datetime
dummy = 'Нет данных'

EUR_COURSE = 74.3
USD_COURSE = 65.1

# поправка на 13% подоходного налога
GROSS_COURSE = 0.87


class HandlerLocation:
    """

        Обработчик адреса

    """
    def __init__(self, raw_data):
        self.lat = raw_data.get('lat') or dummy
        self.lng = raw_data.get('lng') or dummy
        self.city = raw_data.get('city') or dummy
        self.metro = HandlerLocation.handle_metro(self, raw_data) or dummy
        self.street = raw_data.get('street') or dummy

    @property
    def location(self):
        return self.metro

    def handle_metro(self, raw_data):
        result = []

        if 'address' in raw_data and raw_data['address']:
            if 'metro' in raw_data:
                metro = raw_data.get('metro')
                if metro:
                    result.append(metro)

            if 'metro_stations' in raw_data['address']:
                for station in raw_data['address']['metro_stations']:
                    if 'station_name' in station:
                        if station['station_name']:
                            result.append(station['station_name'])
        self.metro = result


class HandleSalary:
    """

        Обработчик зарплаты

    """
    def __init__(self, raw_data):
        self.salary_from = 0
        self.salary_to = 0

        if raw_data.get('salary'):
            scale = 1

            currency = raw_data['salary'].get('currency', 'RUR')

            if currency == 'USD':
                scale = 1 / USD_COURSE
            elif currency == 'EUR':
                scale = 1 / EUR_COURSE

            gross = raw_data['salary'].get('gross', False)

            if gross:
                scale = scale * GROSS_COURSE

            if raw_data['salary'].get('from'):
                self.salary_from = int(raw_data['salary']['from'] * scale / 1000)

            if raw_data['salary'].get('to'):
                self.salary_to = int(raw_data['salary']['to'] * scale / 1000)

    @property
    def salary(self):
        if self.salary_from and self.salary_to:
            return f'{str(self.salary_from)}к-{str(self.salary_to)}к'.center(9)

        elif self.salary_from and not self.salary_to:
            return f'от {str(self.salary_from)}к'.center(9)

        elif not self.salary_from and self.salary_to:
            return f'до {str(self.salary_to)}к'.center(9)
        else:
            return dummy.center(9)

    @property
    def avg_salary(self):
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) // 2

        elif self.salary_from and not self.salary_to:
            return self.salary_from

        elif not self.salary_from and self.salary_to:
            return self.salary_to
        else:
            return 0


class HandleSnippets:
    """

        Обработчик сниппетов

    """
    def __init__(self, raw_data):

        if 'snippet' in raw_data:

            if 'requirement' in raw_data['snippet']:
                self._requirement = raw_data['snippet']['requirement'] or dummy
            else:
                self._requirement = dummy

            if 'responsibility' in raw_data['snippet']:
                self._responsibility = raw_data['snippet']['responsibility'] or dummy
            else:
                self._responsibility = dummy
        else:
            self._requirement = dummy
            self._responsibility = dummy

    @property
    def requirement(self):
        text = self._requirement.replace('<highlighttext>', '')
        text = text.replace('</highlighttext>', '')
        return text

    @property
    def responsibility(self):
        text = self._responsibility.replace('<highlighttext>', '')
        text = text.replace('</highlighttext>', '')
        return text


class HandleEmployer:
    """

        Обработчик работодателя

    """
    def __init__(self, raw_data):
        if 'employer' in raw_data:
            self.id = raw_data['employer'].get('id', dummy)
            self.name = raw_data['employer'].get('name', dummy)
            self.url = raw_data['employer'].get('alternate_url', dummy)
            if raw_data['employer'].get('logo_urls'):
                self.logo = raw_data['employer']['logo_urls'].get('original', dummy)
            else:
                self.logo = dummy
        else:
            self.url = dummy
            self.id = dummy
            self.logo = dummy
            self.name = dummy

    @property
    def employer(self):
        return self.id + ' ' + self.name + ' ' + self.url

    @property
    def logo_url(self):
        return self.logo


class HandleDate:
    """

        Обработчик даты

    """
    def __init__(self, raw_data):
        self._date = None
        if 'published_at' in raw_data:
            # 2018-11-13T12:41:17+0300
            raw_date = raw_data['published_at']
            self._date = datetime.datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S+%f")

    @property
    def date(self):
        if self._date:
            return self._date.strftime("%m/%b/%Y")
        return dummy
