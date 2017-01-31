import json
import math
import sys


def load_data(filepath):
    try:
        with open(filepath, encoding='windows-1251') as bars_file:
            return json.load(bars_file)
    except (OSError, json.JSONDecodeError):
        return


def get_biggest_bar(bars_data):
    return max(bars_data, key=lambda each_bar: each_bar['SeatsCount'])


def get_smallest_bar(bars_data):
    return min(bars_data, key=lambda each_bar: each_bar['SeatsCount'])


def get_closest_bar(bars_data, longitude, latitude):
    return min(bars_data, key=lambda each_bar: get_distance(each_bar['Latitude_WGS84'], each_bar['Longitude_WGS84'],
                                                            latitude, longitude))


def get_distance(latitude_point1, longitude_point1, latitude_point2, longitude_point2):
    """
    Использую формулу расстояний между двумя точками на плоскости. Для небольших расстояний (в пределах города)!
    """
    return math.sqrt((float(latitude_point2) - float(latitude_point1)) ** 2 +
                     (float(longitude_point2) - float(longitude_point1)) ** 2)


def get_float_from_user(message_to_user):
    try:
        # В России принято использовать запятую как разделитель, поэтому позаботимся о пользователе.
        return float(input(message_to_user).replace(',', '.'))
    except ValueError:
        return


def print_bar_information(title, bar):
    bar_string = '{bar[Name]} по-адресу: {bar[Address]} [{bar[Latitude_WGS84]}, {bar[Longitude_WGS84]}]'.format(bar=bar)
    print('{} {}'.format(title, bar_string))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit('Запуск скрипта: python bars.py <пусть-к-json-файлу>')
        
    bars_json = load_data(sys.argv[1])
    if not bars_json:
        sys.exit('Не удаётся загрузить файл {}'.format(sys.argv[1]))

    print_bar_information('Самый большой бар:', get_biggest_bar(bars_json))
    print_bar_information('Самый маленький бар:', get_smallest_bar(bars_json))

    print('Пожалуйста, введите свои координаты:')
    user_latitude = get_float_from_user('Широта: ')
    user_longitude = get_float_from_user('Долгота: ')
    if user_latitude is None or user_longitude is None:
        sys.exit('Ошибка при вводе координат. Перезапустите скрипт.')
    print_bar_information('Ближайший к вам бар:', get_closest_bar(bars_json,
                                                                  latitude=user_latitude,
                                                                  longitude=user_longitude))
