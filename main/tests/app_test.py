import doctest
from unittest import TestCase, main
from main import app


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(app))
    return tests


class GetHourPriceTest(TestCase):
    def test_packer(self):
        self.assertEqual(app.get_hour_price('Упаковщик'), 89)
        self.assertEqual(app.get_hour_price('234'), 89)
        self.assertEqual(app.get_hour_price(''), 89)

    def test_storekeeper(self):
        self.assertEqual(app.get_hour_price('Кладовщик'), 91)

    def test_min_storekeeper(self):
        self.assertEqual(app.get_hour_price('Пом.кладовщика'), 90)


class SalaryOfOneDayTest(TestCase):

    def test_packer_empty_hour(self):
        with self.assertRaises(TypeError) as e:
            app.salary_of_one_day('Упаковка', pos='100', h='', inc_pos=100)
        self.assertEqual('Дожно быть число, а не пустая строка', e.exception.args[0])

    def test_packer_empty_pos(self):
        with self.assertRaises(TypeError) as e:
            app.salary_of_one_day('Упаковка', pos='', h=10, inc_pos=100)
        self.assertEqual('Дожно быть число, а не пустая строка', e.exception.args[0])


class RenderDateTest(TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError) as e:
            app.render_date('')
        self.assertEqual('Дата должна быть в формате гггг-мм-дд', e.exception.args[0])


if __name__ == '__main__':
    main()
