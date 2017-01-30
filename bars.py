import json
import math
import sys


def load_data(filepath):
    try:
        with open(filepath, encoding='windows-1251') as bars_file:
            return json.load(bars_file)
    except OSError:
        print('Не получается открыть указанный файл.')
    except json.JSONDecodeError:
        print('Указанный файл не содержит данных или повреждён.')
    sys.exit(1)


def get_biggest_bar(bars_data):
    return max(bars_data, key=lambda each_bar: each_bar['SeatsCount'])


def get_smallest_bar(bars_data):
    return min(bars_data, key=lambda each_bar: each_bar['SeatsCount'])


def get_closest_bar(bars_data, longitude, latitude):
    return min(bars_data, key=lambda each_bar: get_distance(each_bar['Latitude_WGS84'], each_bar['Longitude_WGS84'],
                                                            latitude, longitude))


def get_distance(latitude_point1, longitude_point1, latitude_point2, longitude_point2):
    """
    Вычисляет расстояние между двумя точками с известными координатами

    :param latitude_point1: широта первой точки
    :param longitude_point1: долгота первой точки
    :param latitude_point2: широта второй точки
    :param longitude_point2: долгота второй точки
    :return: расстояние между точками

    Для расчётов в пределах одного города буду использовать приблизительную модель - весь город находится на плоскости,
    а широта и долгота - это координаты X и Y, и расстояние между ними считается простой формулой.
    А так как выводить его не нужно, то и переводить в метры или километры - тоже.
    """
    return math.sqrt((latitude_point2 - latitude_point1) ** 2 + (longitude_point2 - longitude_point1) ** 2)


def check_script_arguments():
    if len(sys.argv) == 1:
        print('Вы не указали файл с данными при запуске')
        sys.exit(1)


def input_float(message_to_user):
    """
    Запрашивает у пользователя число. При неправильном вводе запрашивает ещё раз.

    :param message_to_user: Сообщение-подсказка пользователю
    :return: введённое число, преобразованное к типу float
    """
    while True:
        try:
            # В России принято использовать запятую как разделитель, поэтому позаботимся о пользователе.
            user_input = float(input(message_to_user).replace(',', '.'))
            break
        except ValueError:
            print('Ошибка при вводе. Попробуйте ещё раз.')
    return user_input


def print_bar_information(title, bar):
    bar_string = '{bar[Name]} по-адресу: {bar[Address]} [{bar[Latitude_WGS84]}, {bar[Longitude_WGS84]}]'.format(bar=bar)
    print('{} {}'.format(title, bar_string))


if __name__ == '__main__':
    check_script_arguments()
    bar_json = load_data(sys.argv[1])
    print_bar_information('Самый большой бар:', get_biggest_bar(bar_json))
    print_bar_information('Самый маленький бар:', get_smallest_bar(bar_json))
    print('Пожалуйста, введите свои координаты:')
    user_latitude = input_float('Широта: ')
    user_longitude = input_float('Долгота: ')
    print_bar_information('Ближайший к вам бар:', get_closest_bar(bar_json,
                                                                  latitude=user_latitude,
                                                                  longitude=user_longitude))