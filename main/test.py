from datetime import datetime, timedelta

from app import (is_valid_password, is_valid_username, is_valid_email, valid_register_data, get_position_price,
                 get_hour_price)
from main.my_database import execute_read_query, connection, current_data

if __name__ == '__main__':
    # Тесты на правильность имени пользователя
    assert (is_valid_username('sdfa adsf')) == False
    assert (is_valid_username('sdfaadsf')) == True
    assert (is_valid_username('sdfa_adsf')) == True
    assert (is_valid_username('sdfa12adsf')) == True
    assert (is_valid_username('sdfa12)adsf')) == False
    assert (is_valid_username('sdfa12)ad_sf')) == False
    assert (is_valid_username('sd____fa12____ad_sf')) == True
    assert (is_valid_username('sd_')) == False
    assert (is_valid_username('111111')) == False
    assert (is_valid_username('11_1111')) == False
    assert (is_valid_username('11в_1111')) == False
    assert (is_valid_username('привет')) == False
    assert (is_valid_username('hello!')) == False
    assert (is_valid_username('')) == False
    assert (is_valid_username('_____')) == False
    assert (is_valid_username('!@#$%^&*()_+')) == False
    assert (is_valid_username('hello')) == True
    assert (is_valid_username('hEEllo')) == True

    # Тесты на правильность пароля
    assert (is_valid_password('12345678')) == True
    assert (is_valid_password('1234567')) == False
    assert (is_valid_password('')) == False
    assert (is_valid_password(' ')) == False
    assert (is_valid_password('qwertyui')) == True
    assert (is_valid_password('qwert*&^%')) == True
    assert (is_valid_password('qwert*&^% ')) == False
    assert (is_valid_password('парольььь')) == False
    assert (is_valid_password('werqwe2342ь')) == False
    assert (is_valid_password('qwert*&^%1')) == True
    assert (is_valid_password('IUIU&^%7657')) == True
    assert (is_valid_password('IsdfIU&^%7657')) == True

    # Тесты на правильность электронной почты
    assert (is_valid_email('sahsa@mail.ru')) == True
    assert (is_valid_email('sa$hsa@mail.ru')) == False
    assert (is_valid_email('sahsa@mail.r2u')) == False
    assert (is_valid_email('sahsa@mail.rwwu')) == False
    assert (is_valid_email('sahsa@@mail.ru')) == False
    assert (is_valid_email('sahsamail.r@u')) == False
    assert (is_valid_email('1111@mail.ru')) == False
    assert (is_valid_email('sahsa@1111.ru')) == False
    assert (is_valid_email('sahsa@____.ru')) == False
    assert (is_valid_email('sa_hsa@mail.ru')) == True
    assert (is_valid_email('____@mail.ru')) == False
    assert (is_valid_email('_d__1_@mail.ru')) == True
    assert (is_valid_email('_HH__1_@mail.ru')) == True
    assert (is_valid_email('_HH__1_@mail.ru')) == True
    assert (is_valid_email('_HH_бб_1_@mail.ru')) == False
    assert (is_valid_email('_HH__1_@mail.ru!')) == False
    assert (is_valid_email('_HH__1_@mail!.ru!')) == False
    assert (is_valid_email('ыфва435')) == False
    assert (is_valid_email('почта@mail.ru')) == False
    assert (is_valid_email('sahsa@mail.ру')) == False
    assert (is_valid_email('sahsa@мэйл.ru')) == False

    # Тесты на проверку всех данных регистрации
    assert valid_register_data('sasha@mail.ru', '1123456678') == True
    assert valid_register_data('sas!ha@mail.ru', '1123456678') == False
    assert valid_register_data('sasha@mail.ru', 'парольььь') == False
    assert valid_register_data('sasha.mail@ru', '1123456678') == False
    assert valid_register_data('sas@ha@mail.ru', '1123456678') == False
    assert valid_register_data('sashamail.ru', '1123456678') == False
    assert valid_register_data('sasha@mail.ru', '1123456UTYU678') == True
    assert valid_register_data('sasha@mail.ru', '11_*&%^23456678') == True
    assert valid_register_data('sasha@mail.ru', '11234566 78') == False
    assert valid_register_data('sasha@mailru', '1123456678') == False

    # Функция возращающая стоимость часа
    assert get_hour_price('Кладовщик') == 91
    assert get_hour_price('Упаковщик') == 89
    assert get_hour_price('Пом.кладовщика') == 90
    assert get_hour_price('') == 89

    # Функция возвращающая стоимость позиции
    assert get_position_price('1 отдел') == 3.7
    assert get_position_price('3 отдел') == 4.7
    assert get_position_price('Упаковка') == 3


    def em(email, month):

        def mon(action):
            nonlocal month
            if action == '+':
                month += 1
            elif action == '-':
                month -= 1

            def res():
                return email + month

            return res()

        return mon


    def test_get_salary_data_month(email: str, cur_data: datetime, connect=connection):
        def f1(action):
            nonlocal cur_data
            if action == '+':

                cur_data = datetime(year=cur_data.year, month=cur_data.month + 1, day=cur_data.day)
            else:
                cur_data = datetime(year=cur_data.year, month=cur_data.month - 1, day=cur_data.day)

            def f2():
                result = execute_read_query(connect,
                                            f'SELECT date, hours, salary, positions, incoming_positions FROM salary_users '
                                            f'WHERE email = "{email}" and '
                                            f'strftime("%m", date) == strftime("%m", "{cur_data}")')
                return result

            return f2()

        return f1


    def test_get_sum_of_month(email: str, cur_data: datetime, connect=connection):
        def f1(action):
            nonlocal cur_data
            if action == '+':

                cur_data = datetime(year=cur_data.year, month=cur_data.month + 1, day=cur_data.day)
            else:
                cur_data = datetime(year=cur_data.year, month=cur_data.month - 1, day=cur_data.day)

            def f2():
                result = execute_read_query(connect,
                                            f'SELECT SUM(salary),SUM(hours), SUM(positions), SUM(incoming_positions) '
                                            f'FROM salary_users WHERE email = "{email}" '
                                            f'and strftime("%m", date) == strftime("%m", "{cur_data}")')
                return result

            return f2()

        return f1

    c_date = current_data
    sal_data = test_get_sum_of_month('max@mail.ru', cur_data=c_date)
    print(sal_data('-'))
    print(sal_data('-'))
    print(sal_data('+'))
    print(sal_data('+'))
