import json
import math
import sys

# Из https://en.wikipedia.org/wiki/Earth_radius#Mean_radius.
# Средний радиус земли, принимаемой за сферу,расчёты с таким приближением
# могут привести к ошибке вычислений порядка 0,5%

EARTH_RADIUS = 6371009  # в метрах


def load_data(filepath):
    try:
        with open(filepath, encoding='windows-1251') as bars_file:
            return json.load(bars_file)
    except OSError:
        print('Не получается открыть указанный файл.')
    except json.JSONDecodeError:
        print('Указанный файл не содержит данных или повреждён.')


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
    :return: расстояние между точками в метрах

    Для расчёта расстояния используется сферическая теорема косинусов.
    """
    # Значения углов должны быть в радианах
    p1_lat = math.radians(float(latitude_point1))
    p1_lon = math.radians(float(longitude_point1))
    p2_lat = math.radians(float(latitude_point2))
    p2_lon = math.radians(float(longitude_point2))

    longitude_delta = p2_lon - p1_lon

    # Эти переменные я расчитываю чтобы не городить трёхэтажную вложенность в основной формуле
    cos_l1 = math.cos(p1_lat)
    cos_l2 = math.cos(p2_lat)
    sin_l1 = math.sin(p1_lat)
    sin_l2 = math.sin(p2_lat)
    cos_delta = math.cos(longitude_delta)
    sin_delta = math.sin(longitude_delta)
    """
    Формула для расчёта угловой разницы https://en.wikipedia.org/wiki/Great-circle_distance
    atan2(y, x) используется вместо простой atan(y/x) т.к. atan2 возвращает результат с учётом четверти,
    в которой находится точка (X, Y).И поэтому результат тоже оказывается в правильной четверти круга.
    """
    y = math.sqrt(math.pow(cos_l2 * sin_delta, 2) + math.pow(cos_l1 * sin_l2 - sin_l1 * cos_l2 * cos_delta, 2))
    x = sin_l1 * sin_l2 + cos_l1 * cos_l2 * cos_delta
    return math.atan2(y, x) * EARTH_RADIUS


def get_bar_info_string(bar):
    return '{bar[Name]} по-адресу: {bar[Address]} [{bar[Latitude_WGS84]}, {bar[Longitude_WGS84]}]'.format(bar=bar)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Вы не указали файл с данными при запуске')
        sys.exit(1)
    bar_json = load_data(sys.argv[1])
    if not bar_json:
        sys.exit(1)
    biggest_bar = get_biggest_bar(bar_json)
    smallest_bar = get_smallest_bar(bar_json)
    print('Самый большой бар: {}'.format(get_bar_info_string(biggest_bar)))
    print('Самый маленький бар: {}'.format(get_bar_info_string(smallest_bar)))
    print('Пожалуйста, введите свои координаты:')
    while True:
        try:
            # В России принято использовать запятую как разделитель, поэтому позаботимся о пользователе.
            user_latitude = float(input('Широта: ').replace(',', '.'))
            break
        except ValueError:
            print('Ошибка при вводе широты. Попробуйте ещё раз.')
    while True:
        try:
            user_longitude = float(input('Долгота: ').replace(',', '.'))
            break
        except ValueError:
            print('Ошибка при вводе долготы. Попробуйте ещё раз.')
    closest_bar = get_closest_bar(bar_json, latitude=user_latitude, longitude=user_longitude)
    print('Ближайший к вам бар: {} '.format(get_bar_info_string(closest_bar)))
