# -*- coding: utf-8 -*-
"""

    Testing module for 'handlers.py'

"""
import unittest
import handlers
import test_full_vacancy
import test_regular_vacancy

vac0 = test_full_vacancy.full_vacancy
vac1 = test_regular_vacancy.vacancy1
vac2 = test_regular_vacancy.vacancy2
vac3 = test_regular_vacancy.vacancy3
vac4 = test_regular_vacancy.vacancy4
vac5 = test_regular_vacancy.vacancy5

good_date0 = (1541607699.03, 1541607699.03, None)
good_date1 = (1539868353.03, 1539868353.03, None)
good_date2 = (1539777204.03, 1539777204.03, None)
good_date3 = (1539874729.03, 1539874729.03, None)
good_date4 = (1539619145.03, 1539619145.03, None)

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


class TestHandlers(unittest.TestCase):

    def test_date(self):
        self.assertEqual(handlers.handle_date(vac0), good_date0)
        self.assertEqual(handlers.handle_date(vac1), good_date1)
        self.assertEqual(handlers.handle_date(vac2), good_date2)
        self.assertEqual(handlers.handle_date(vac3), good_date3)
        self.assertEqual(handlers.handle_date(vac4), good_date4)

    def test_salary(self):
        # TODO - добавить коррекцию для курсов валют
        # TODO - добавить дополнительные валюты
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


if __name__ == '__main__':
    unittest.main()
