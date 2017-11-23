from .countries import *


def n_tuple(n, first=[], last=[]):
    return tuple(first + [(i, i) for i in range(1, n)] + last)


CATEGORIES = [
    (1, 'Culture'),
    (2, 'Work hand'),
    (3, 'Language exchange'),
    (4, 'Art'),
    (5, 'Other'),
]

HOUSE_TYPES = [
    (1, 'Apartment'),
    (2, 'House'),
    (3, 'Guesthouse'),
    (4, 'Office'),
    (5, 'Dormitory'),
]

ROOM_TYPES = [
    (1, 'Private room'),
    (2, 'Shared room'),
]

MEAL_TYPES = [
    (1, 'It\'s a deal! We share a meal!'),
    (2, 'Make your dishes using host\'s ingredient'),
]

INTERNET_TYPES = [
    (1, 'Wifi'),
    (2, 'Only LAN'),
    (3, 'No Internet'),
]

CAPACITIES = n_tuple(10)
MIN_STAY = n_tuple(90)
MAX_STAY = n_tuple(60, first=[(0, 'Unlimited')])
