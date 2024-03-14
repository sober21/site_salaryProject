from datetime import datetime
from unittest import main, TestCase

from main.app import get_hour_price


class GetHourPriceTest(TestCase):
    def test_packer(self):
        self.assertEqual(get_hour_price('Упаковщик'), 89)
        self.assertEqual(get_hour_price('234'), 89)
        self.assertEqual(get_hour_price(''), 89)

    def test_storekeeper(self):
        self.assertEqual(get_hour_price('Кладовщик'), 91)

    def test_min_storekeeper(self):
        self.assertEqual(get_hour_price('Пом.кладовщика'), 90)


if __name__ == '__main__':
    main()
