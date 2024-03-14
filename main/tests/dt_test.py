from datetime import datetime
from unittest import main, TestCase
from main.app import render_date


class RenderDateTest(TestCase):
    def test_get_str(self):
        self.assertEqual(render_date('2024-03-14'), '14 Марта')

    def test_get_datetime(self):
        self.assertEqual(render_date(datetime(year=2024, month=3, day=14)), '14 Марта')

    def test_get_date(self):
        self.assertEqual(render_date(datetime(year=2024, month=3, day=14).date()), '14 Марта')

    def test_empty(self):
        with self.assertRaises(ValueError) as e:
            render_date('')
        self.assertEqual('Дата должна быть в формате гггг-мм-дд', e.exception.args[0])


if __name__ == '__main__':
    main()
