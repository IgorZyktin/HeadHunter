# -*- coding: utf-8 -*-
"""

    Тесты модуля 'handlers.py'

"""
from mock import Mock, patch
import unittest
import handlers
import time
import math


in_time0 = None
in_time1 = {}
in_time2 = {'created_at': ''}
in_time3 = {'published_at': ''}
in_time4 = {'created_at': 'asdasd'}
in_time5 = {'published_at': 'asdasd'}
in_time6 = {'created_at': '2018-11-07T19:21:39+0300'}
in_time7 = {'created_at': '2018-11-07T19:21:39+0300', 'published_at': '2018-11-07T19:21:39+0300'}
in_time8 = {'created_at': '', 'published_at': ''}
in_time9 = {'created_at': None, 'published_at': None}

mock_time = Mock()
mock_time.return_value = time.time()

out_time_0 = (None, None, mock_time.return_value)
out_time_1 = (None, None, mock_time.return_value)
out_time_2 = (None, None, mock_time.return_value)
out_time_3 = (None, None, mock_time.return_value)
out_time_4 = (None, None, mock_time.return_value)
out_time_5 = (None, None, mock_time.return_value)
out_time_6 = (1541607699.03, None, mock_time.return_value)
out_time_7 = (1541607699.03, 1541607699.03, mock_time.return_value)
out_time_8 = (None, None, mock_time.return_value)
out_time_9 = (None, None, mock_time.return_value)

in_salary_0 = None
in_salary_1 = {"salary": {}}
in_salary_2 = {"salary": None}
in_salary_3 = {"salary": {"from": None, "to": None, "currency": None, "gross": None}}
in_salary_4 = {"salary": {"from": 1000, "to": None, "currency": None, "gross": None}}
in_salary_5 = {"salary": {"from": None, "to": 2000, "currency": None, "gross": None}}
in_salary_6 = {"salary": {"from": 1000, "to": 2000, "currency": 'RUR', "gross": False}}
in_salary_7 = {"salary": {"from": 1000, "to": 2000, "currency": None, "gross": False}}
in_salary_8 = {"salary": {"from": 1000, "to": 2000, "currency": 'RUR', "gross": True}}
in_salary_9 = {"salary": {"from": 100000, "to": None, "currency": 'RUR', "gross": None}}
in_salary_10 = {"salary": {"from": 1000, "to": 2000, "currency": 'EUR', "gross": True}}
in_salary_11 = {"salary": {"from": None, "to": 2000, "currency": 'EUR', "gross": False}}
in_salary_12 = {"salary": {"from": 1000, "to": None, "currency": 'USD', "gross": True}}
in_salary_13 = {"salary": {"from": 1000, "to": 2000, "currency": 'USD', "gross": False}}

gross_1000 = int(math.floor(1000 * handlers.GROSS_COURSE))
gross_1500 = int(math.floor(1500 * handlers.GROSS_COURSE))
gross_2000 = int(math.floor(2000 * handlers.GROSS_COURSE))

eur_no_gr_1000 = int(math.floor(1000 * handlers.EUR_COURSE))
eur_no_gr_1500 = int(math.floor(1500 * handlers.EUR_COURSE))
eur_no_gr_2000 = int(math.floor(2000 * handlers.EUR_COURSE))

eur_1000 = int(math.floor(1000 * handlers.EUR_COURSE * handlers.GROSS_COURSE))
eur_1500 = int(math.floor(1500 * handlers.EUR_COURSE * handlers.GROSS_COURSE))
eur_2000 = int(math.floor(2000 * handlers.EUR_COURSE * handlers.GROSS_COURSE))

usd_no_gr_1000 = int(math.floor(1000 * handlers.USD_COURSE))
usd_no_gr_1500 = int(math.floor(1500 * handlers.USD_COURSE))
usd_no_gr_2000 = int(math.floor(2000 * handlers.USD_COURSE))

usd_1000 = int(math.floor(1000 * handlers.USD_COURSE * handlers.GROSS_COURSE))
usd_1500 = int(math.floor(1500 * handlers.USD_COURSE * handlers.GROSS_COURSE))
usd_2000 = int(math.floor(2000 * handlers.USD_COURSE * handlers.GROSS_COURSE))

eur_1k_2k = f' {int(eur_1000/1000)}к-{int(eur_2000/1000)}к'
eur_2k = f' до {int(eur_no_gr_2000/1000)}к '

out_salary_0 = (None, None, 0, 'Нет данных')
out_salary_1 = (None, None, 0, 'Нет данных')
out_salary_2 = (None, None, 0, 'Нет данных')
out_salary_3 = (None, None, 0, 'Нет данных')
out_salary_4 = (-1000, None, -1000, '  от -1к ')
out_salary_5 = (None, -2000, -2000, '  до -2к ')
out_salary_6 = (1000, 2000, 1500, '  1к-2к  ')
out_salary_7 = (-1000, -2000, -1500, ' -1к--2к ')
out_salary_8 = (gross_1000, gross_2000, gross_1500, '  0к-1к  ')
out_salary_9 = (100000, None, 100000, ' от 100к ')
out_salary_10 = (eur_1000 - 1, eur_2000 - 1, eur_1500 - 1, eur_1k_2k)
out_salary_11 = (None, eur_no_gr_2000, eur_no_gr_2000, eur_2k)
out_salary_12 = (usd_1000, None, usd_1000, '  от 56к ')
out_salary_13 = (usd_no_gr_1000, usd_no_gr_2000, usd_no_gr_1500, ' 65к-130к')

in_address_1 = None
in_address_2 = {}
in_address_3 = {"address": {}}
in_address_4 = {"address": None, 'area': None}
in_address_5 = {"address": {"city": 'some_city', "street": None}, 'area': {'name': 'Пекин'}}
in_address_6 = {"address": {"city": None, "street": "some_street"}}
in_address_7 = {"address": {"city": None, "street": "some_street"}, 'area': {'name': 'Пекин'}}
in_address_8 = {"address": {"city": 'some_city', 'street': 'some_street'}}

in_address_9 = {"address": {"city": 'some_city',
                            'street': 'some_street'},
                'area': {'name': 'Пекин'}}

out_address_1 = (None, None)
out_address_2 = (None, None)
out_address_3 = (None, None)
out_address_4 = (None, None)
out_address_5 = ('some_city', None)
out_address_6 = (None, 'some_street')
out_address_7 = ('Пекин', 'some_street')
out_address_8 = ('some_city', 'some_street')
out_address_9 = ('some_city', 'some_street')

in_employer_1 = None
in_employer_2 = {"employer": None}
in_employer_3 = {"employer": {}}
in_employer_4 = {"employer": {"id": 12345}}
in_employer_5 = {"employer": {"id": '12345'}}
in_employer_6 = {"employer": {"id": '12345', "name": "some", "alternate_url": "www.ru"}}
in_employer_7 = {"employer": {"id": None, "name": None, "alternate_url": None}}
in_employer_8 = {"employer": {"id": '', "name": '', "alternate_url": ''}}

out_employer_1 = (None, None, None)
out_employer_2 = (None, None, None)
out_employer_3 = (None, None, None)
out_employer_4 = (12345, None, None)
out_employer_5 = (12345, None, None)
out_employer_6 = (12345, 'www.ru', 'some')
out_employer_7 = (None, None, None)
out_employer_8 = (None, None, None)

in_info_1 = None
in_info_2 = {"description": ''}
in_info_3 = {"description": None}
in_info_4 = {"description": '', "experience": '', "key_skills": '',
             "snippet": {"requirement": "", "responsibility": ''}}
in_info_5 = {"description": '', "experience": '', "key_skills": '',
             "snippet": {"requirement": "", "responsibility": ''}}
in_info_6 = {"description": None, "experience": None, "key_skills": None,
             "snippet": {"requirement": None, "responsibility": None}}

in_info_7 = {"description": 'some',
             "experience": 'some',
             "key_skills": ['some_skill', 'some_skill'],
             "snippet": {"requirement": "some", "responsibility": 'some'}}

in_info_8 = {"description": 'some',
             "experience": 'some',
             "key_skills": None,
             "snippet": {"requirement": "some"}}

in_info_9 = {"description": 'some',
             "experience": 'some',
             "key_skills": 'some',
             "snippet": {"requirement": "some", "responsibility": 'some'}}

in_info_10 = {"description": 'some',
             "experience": 'some',
             "key_skills": {'name': {}},
             "snippet": {"requirement": "some", "responsibility": 'some'}}

in_info_11 = {"description": 'some',
             "experience": 'some',
             "key_skills": [{'name': 'some_skill'}],
             "snippet": {"requirement": "some", "responsibility": 'some'}}

in_info_12 = {"description": 'some',
             "experience": 'some',
             "key_skills": [{'name': 'sk1'}, {'name': 'sk2'}],
             "snippet": {"requirement": "some", "responsibility": 'some'}}

out_info_1 = (None, None, None, None)
out_info_2 = (None, None, None, None)
out_info_3 = (None, None, None, None)
out_info_4 = (None, None, None, None)
out_info_5 = (None, None, None, None)
out_info_6 = (None, None, None, None)
out_info_7 = ('some', None, 'some', 'some some')
out_info_8 = ('some', None, 'some', 'some')
out_info_9 = ('some', None, 'some', 'some some')
out_info_10 = ('some', None, 'some', 'some some')
out_info_11 = ('some', 'some_skill', 'some', 'some some')
out_info_12 = ('some', 'sk1, sk2', 'some', 'some some')


class TestHandlers(unittest.TestCase):

    @patch('time.time', mock_time)
    def test_date(self):
        self.assertEqual(handlers.handle_time(in_time0), out_time_0)
        self.assertEqual(handlers.handle_time(in_time1), out_time_1)
        self.assertEqual(handlers.handle_time(in_time2), out_time_2)
        self.assertEqual(handlers.handle_time(in_time3), out_time_3)
        self.assertEqual(handlers.handle_time(in_time4), out_time_4)
        self.assertEqual(handlers.handle_time(in_time5), out_time_5)
        self.assertEqual(handlers.handle_time(in_time6), out_time_6)
        self.assertEqual(handlers.handle_time(in_time7), out_time_7)
        self.assertEqual(handlers.handle_time(in_time8), out_time_8)
        self.assertEqual(handlers.handle_time(in_time9), out_time_9)

    def test_salary(self):
        # TODO - добавить коррекцию для курсов валют
        # TODO - добавить дополнительные валюты
        self.assertEqual(handlers.handle_salary(in_salary_0), out_salary_0)
        self.assertEqual(handlers.handle_salary(in_salary_1), out_salary_1)
        self.assertEqual(handlers.handle_salary(in_salary_2), out_salary_2)
        self.assertEqual(handlers.handle_salary(in_salary_3), out_salary_3)
        self.assertEqual(handlers.handle_salary(in_salary_4), out_salary_4)
        self.assertEqual(handlers.handle_salary(in_salary_5), out_salary_5)
        self.assertEqual(handlers.handle_salary(in_salary_6), out_salary_6)
        self.assertEqual(handlers.handle_salary(in_salary_7), out_salary_7)
        self.assertEqual(handlers.handle_salary(in_salary_8), out_salary_8)
        self.assertEqual(handlers.handle_salary(in_salary_9), out_salary_9)
        self.assertEqual(handlers.handle_salary(in_salary_10), out_salary_10)
        self.assertEqual(handlers.handle_salary(in_salary_11), out_salary_11)
        self.assertEqual(handlers.handle_salary(in_salary_12), out_salary_12)
        self.assertEqual(handlers.handle_salary(in_salary_13), out_salary_13)

    def test_handle_location(self):
        self.assertEqual(handlers.handle_location(in_address_1), out_address_1)
        self.assertEqual(handlers.handle_location(in_address_2), out_address_2)
        self.assertEqual(handlers.handle_location(in_address_3), out_address_3)
        self.assertEqual(handlers.handle_location(in_address_4), out_address_4)
        self.assertEqual(handlers.handle_location(in_address_5), out_address_5)
        self.assertEqual(handlers.handle_location(in_address_6), out_address_6)
        self.assertEqual(handlers.handle_location(in_address_7), out_address_7)
        self.assertEqual(handlers.handle_location(in_address_8), out_address_8)
        self.assertEqual(handlers.handle_location(in_address_9), out_address_9)

    def test_handle_employer(self):
        self.assertEqual(handlers.handle_employer(in_employer_1), out_employer_1)
        self.assertEqual(handlers.handle_employer(in_employer_2), out_employer_2)
        self.assertEqual(handlers.handle_employer(in_employer_3), out_employer_3)
        self.assertEqual(handlers.handle_employer(in_employer_4), out_employer_4)
        self.assertEqual(handlers.handle_employer(in_employer_5), out_employer_5)
        self.assertEqual(handlers.handle_employer(in_employer_6), out_employer_6)
        self.assertEqual(handlers.handle_employer(in_employer_7), out_employer_7)
        self.assertEqual(handlers.handle_employer(in_employer_8), out_employer_8)

    def test_handle_info(self):
        self.assertEqual(handlers.handle_info(in_info_1), out_info_1)
        self.assertEqual(handlers.handle_info(in_info_2), out_info_2)
        self.assertEqual(handlers.handle_info(in_info_3), out_info_3)
        self.assertEqual(handlers.handle_info(in_info_4), out_info_4)
        self.assertEqual(handlers.handle_info(in_info_5), out_info_5)
        self.assertEqual(handlers.handle_info(in_info_6), out_info_6)
        self.assertEqual(handlers.handle_info(in_info_7), out_info_7)
        self.assertEqual(handlers.handle_info(in_info_8), out_info_8)
        self.assertEqual(handlers.handle_info(in_info_9), out_info_9)
        self.assertEqual(handlers.handle_info(in_info_10), out_info_10)
        self.assertEqual(handlers.handle_info(in_info_11), out_info_11)
        self.assertEqual(handlers.handle_info(in_info_12), out_info_12)


if __name__ == '__main__':
    unittest.main()
