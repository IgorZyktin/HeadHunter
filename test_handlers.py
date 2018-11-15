# -*- coding: utf-8 -*-
"""

    Тесты модуля 'handlers.py'

"""
import unittest
import handlers

time1 = {'created_at': '2018-11-07T19:21:39+0300'}

time2 = {'created_at': '2018-11-07T19:21:39+0300',
         'published_at': '',
         'edited_at': '2018-11-07T19:21:39+0300'}

time3 = {'created_at': None,
         'published_at': '2018-11-07T19:21:39+0300',
         'edited_at': None}

time4 = {'created_at': '',
         'published_at': '2018-11-07T19:21:39+0300',
         'edited_at': '2018-11-07T19:21:39+0300'}

time5 = {'created_at': '2018-11-07T19:21:39+0300',
         'published_at': '2018-11-07T19:21:39+0300',
         'edited_at': '2018-11-07T19:21:39+0300'}

salary_1 = {"salary": {"from": None, "to": None, "currency": None, "gross": None}}
salary_2 = {"salary": {"from": 1000, "to": None, "currency": None, "gross": None}}
salary_3 = {"salary": {"from": None, "to": 2000, "currency": None, "gross": None}}
salary_4 = {"salary": {"from": 1000, "to": 2000, "currency": 'RUR', "gross": False}}
salary_5 = {"salary": {"from": 1000, "to": 2000, "currency": None, "gross": False}}
salary_6 = {"salary": {"from": 1000, "to": 2000, "currency": 'RUR', "gross": True}}
salary_7 = {"salary": {"from": 100000, "to": None, "currency": 'RUR', "gross": None}}
salary_8 = {"salary": {"from": 1000, "to": 2000, "currency": 'EUR', "gross": True}}
salary_9 = {"salary": {"from": None, "to": 2000, "currency": 'EUR', "gross": False}}
salary_10 = {"salary": {"from": 1000, "to": None, "currency": 'USD', "gross": True}}
salary_11 = {"salary": {"from": 1000, "to": 2000, "currency": 'USD', "gross": False}}
salary_12 = {"salary": {}}

address1 = {"address": {"city": 'some_city', "street": "some_street"}}
address2 = {"address": {"city": '', "street": ""}}
address3 = {"address": {"city": 'some_city', "street": None}}
address4 = {"address": {"city": None, "street": "some_street"}}
address5 = {"address": {"city": None}}

employer1 = None
employer2 = {"employer": {"id": 12345}}
employer3 = {"employer": {"id": '12345',
                          "name": "some",
                          "alternate_url": "www.ru",
                          "logo_urls": {'original': "www.com"}}}
employer4 = {"employer": {"id": 12345, "name": None}}
employer5 = {"employer": {"id": None}}

info1 = None
info2 = {"description": 'some',
         "experience": 'some',
         "key_skills": 'some',
         "snippet": {"requirement": "some", "responsibility": 'some'}}

info3 = {"description": 'some',
         "experience": 'some',
         "key_skills": None,
         "snippet": {"requirement": "some"}}

info4 = {"description": 'some',
         "experience": 'some',
         "key_skills": 'some',
         "snippet": {"requirement": "some", "responsibility": 'some'}}

info5 = {"description": 'some',
         "experience": 'some',
         "key_skills": {'name'},
         "snippet": {"requirement": "some", "responsibility": 'some'}}

info6 = {"description": 'some',
         "experience": 'some',
         "key_skills": 'some',
         "snippet": {"requirement": "some", "responsibility": 'some'}}

info7 = {"description": 'some',
         "experience": 'some',
         "key_skills": [{'name': 'sk1'}, {'name': 'sk2'}],
         "snippet": {"requirement": "some", "responsibility": 'some'}}


class TestHandlers(unittest.TestCase):

    def test_date(self):
        self.assertEqual(handlers.handle_date(None), (None, None, None))
        self.assertEqual(handlers.handle_date(time1), (1541607699.03, None, None))
        self.assertEqual(handlers.handle_date(time2), (1541607699.03, None, 1541607699.03))
        self.assertEqual(handlers.handle_date(time3), (None, 1541607699.03, None))
        self.assertEqual(handlers.handle_date(time4), (None, 1541607699.03, 1541607699.03))
        self.assertEqual(handlers.handle_date(time5), (1541607699.03, 1541607699.03, 1541607699.03))

    def test_salary(self):
        # TODO - добавить коррекцию для курсов валют
        # TODO - добавить дополнительные валюты
        self.assertEqual(handlers.handle_salary(None), (None, None, 0, 'Нет данных'))
        self.assertEqual(handlers.handle_salary(salary_1), (None, None, 0, 'Нет данных'))
        self.assertEqual(handlers.handle_salary(salary_2), (-1000, None, -1000, '  от -1к '))
        self.assertEqual(handlers.handle_salary(salary_3), (None, -2000, -2000, 'до -2000к'))
        self.assertEqual(handlers.handle_salary(salary_4), (1000, 2000, 1500, '  1к-2к  '))
        self.assertEqual(handlers.handle_salary(salary_5), (-1000, -2000, -1500, ' -1к--2к '))
        self.assertEqual(handlers.handle_salary(salary_6), (870, 1740, 1305, '  0к-1к  '))
        self.assertEqual(handlers.handle_salary(salary_7), (100000, None, 100000, ' от 100к '))
        self.assertEqual(handlers.handle_salary(salary_8), (64640, 129281, 96960, ' 64к-129к'))
        self.assertEqual(handlers.handle_salary(salary_9), (None, 148600, 148600, 'до 148600к'))
        self.assertEqual(handlers.handle_salary(salary_10), (56636, None, 56636, '  от 56к '))
        self.assertEqual(handlers.handle_salary(salary_11), (65099, 130199, 97649, ' 65к-130к'))
        self.assertEqual(handlers.handle_salary(salary_12), (None, None, 0, 'Нет данных'))

    def test_handle_location(self):
        self.assertEqual(handlers.handle_location(None), (None, None))
        self.assertEqual(handlers.handle_location(address1), ('some_city', 'some_street'))
        self.assertEqual(handlers.handle_location(address2), (None, None))
        self.assertEqual(handlers.handle_location(address3), ('some_city', None))
        self.assertEqual(handlers.handle_location(address4), (None, 'some_street'))
        self.assertEqual(handlers.handle_location(address5), (None, None))
        self.assertEqual(handlers.handle_location({}), (None, None))

    def test_handle_employer(self):
        self.assertEqual(handlers.handle_employer(employer1), (None, None, None, None))
        self.assertEqual(handlers.handle_employer(employer2), (12345, None, None, None))
        self.assertEqual(handlers.handle_employer(employer3), (12345, 'some', 'www.ru', 'www.com'))
        self.assertEqual(handlers.handle_employer(employer4), (12345, None, None, None))
        self.assertEqual(handlers.handle_employer(employer5), (None, None, None, None))

    def test_handle_info(self):
        self.assertEqual(handlers.handle_info(info1), (None, None, None, None))
        self.assertEqual(handlers.handle_info(info2), ('some', None, 'some', 'some some'))
        self.assertEqual(handlers.handle_info(info3), ('some', None, 'some', 'some'))
        self.assertEqual(handlers.handle_info(info4), ('some', None, 'some', 'some some'))
        self.assertEqual(handlers.handle_info(info5), ('some', None, 'some', 'some some'))
        self.assertEqual(handlers.handle_info(info6), ('some', None, 'some', 'some some'))
        self.assertEqual(handlers.handle_info(info7), ('some', 'sk1, sk2', 'some', 'some some'))


if __name__ == '__main__':
    unittest.main()
