from datetime import datetime, date, timedelta
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

PRICE_OF_HOUR = 91
PRICE_OF_POSITION = 3.7

current_data = date.today()


def salary_of_one_day(h, pos, emp) -> int | float:
    # Считает зарплату за один день и возвращает число
    salary = int(h) * PRICE_OF_HOUR + (int(pos) / int(emp)) * PRICE_OF_POSITION
    return salary


def get_last_date(file: str) -> datetime:
    '''Возаращает последнюю дату из файла'''
    with open(file, encoding='utf-8') as file_for_read:
        lst = file_for_read.readlines()
        year = ''
        for line in lst:
            if line.strip().endswith(' год'):
                year = line.strip().split()[0]
        last_writer = str(year) + ' ' + lst[-1].split(':')[0]  # берём из последней строки только дату
        last_date = datetime.strptime(last_writer, '%Y %d %B')
    return last_date


def empty_file(file: str) -> bool:
    '''проверяет - является ли файл пустым'''
    with open(file, encoding='utf-8') as f:
        try:
            next(f)
            return False
        except StopIteration:
            return True


def layaway_list(c_date: datetime, l_date: datetime) -> list:
    '''Возвращает список нерабочих дней, который надо будет записать в файл'''
    cur_date = c_date
    last_date = l_date + timedelta(days=1)
    res = []
    cur_month, cur_year = last_date.month, last_date.year
    while cur_date > last_date:
        if cur_year != last_date.year:
            cur_year = last_date.year
            res.append(f'{cur_year} год\n')
        if cur_month != last_date.month:
            cur_month = last_date.month
            res.append(f'{last_date.strftime("%B")}\n')

        res.append(f'{last_date.strftime("%d %B")}: выходной.\n')
        last_date += timedelta(days=1)

    return res


def valid_year(c, l):
    pass


def valid_month(c):
    pass


def write_in_file(sal) -> None:
    '''Записывет данные в файл'''
    file = 'for_text_files/salary1.txt'

    with open(file, 'a', encoding='utf-8') as file_for_write:
        cur_date = datetime.today()
        cur_date = datetime(year=cur_date.year, month=cur_date.month, day=cur_date.day)
        empty_f = empty_file(file)
        if empty_f:  # если файл пустой
            year = cur_date.year
            month = cur_date.strftime('%B')
            print(f'{year} год', file=file_for_write)
            print(f'{month}', file=file_for_write)
        else:
            last_date = get_last_date(file)

            if cur_date > last_date + timedelta(days=1):
                missed_days = layaway_list(cur_date, last_date)
                file_for_write.writelines(missed_days)
            else:
                if cur_date.year > last_date.year:
                    month = cur_date.strftime('%B')
                    print(f'{cur_date.year} год', file=file_for_write)
                    print(f'{month}', file=file_for_write)
                elif cur_date.month > last_date.month:
                    month = cur_date.strftime('%B')
                    print(f'{month}', file=file_for_write)
        cur_date = cur_date.strftime('%d %B')
        print(f'{cur_date}: {int(sal)} руб.', file=file_for_write)


def input_dates() -> tuple[int, int, int]:
    '''Получает и возваращает входные данные'''
    while True:
        try:
            hours = input('Часы:')
            positions = input('Количество позиций:')
            employee = input('Количество человек:')
            if hours == '':
                hours = '9'
            if positions == '':
                positions = '1'
            if employee == '':
                employee = '3'
            if not (hours + positions + employee).isdigit():
                raise TypeError
            break
        except TypeError:
            print('Введите число либо пустую строку.')
    hours, positions, employee = int(hours), int(positions), int(employee)
    return hours, positions, employee


def main():
    hours, positions, employee = input_dates()
    salary = salary_of_one_day(hours, positions, employee)
    write_in_file(salary)


if __name__ == '__main__':
    # cur = datetime.today()
    # cur = datetime(day=cur.day, month=cur.month, year=cur.year)
    # last = datetime(year=2024, month=2, day=7)
    # print(layaway_list(cur, last))
    main()
