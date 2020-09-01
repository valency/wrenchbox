import json
import random
import string
import sys
import time
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_DOWN
from heapq import heappush, heappop
from math import pi



def digits(n):
    """
    Count the digits of a given float number
    :param n: the float number
    :return: number of digits
    """
    return len(str(n).split('.')[-1])


def random_chars(n):
    """
    Generate a random string from a-zA-Z0-9
    :param n: length of the string
    :return: the random string
    """
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(n))


def random_letters(n):
    """
    Generate a random string from a-zA-Z
    :param n: length of the string
    :return: the random string
    """
    return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(n))


def random_numbers(n):
    """
    Generate a random string from 0-9
    :param n: length of the string
    :return: the random string
    """
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(n))






def string_insert(str1, str2, i):
    """
    Insert a string in the middle of another string
    :param str1: the original string
    :param str2: the string to be inserted
    :param i: the index of the insertion position
    :return: the resulting string
    """
    return str1[:i] + str2 + str1[i:]




if __name__ == "__main__":
    print(digits(pi))
    print(decimal_safe(pi), decimal_safe(str(pi)))
    print(decimal_round(pi, 0.5), decimal_round(pi + 0.5, 0.5))
    print(random_chars(3))
    print(random_letters(3))
    print(random_numbers(3))
    print(dict_retrieve_keys({'a': 1, 'b': {'a': 3, 'b': 4}}, 'a'))
    print(dict_search([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}], 'a', 1))
    print(dict_merge([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}], [{'a': 1, 'b': 3}, {'a': 2, 'b': 4}], 'a'))
    print(dict_sort([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 1, 'b': 3}, {'a': 2, 'b': 4}], 'a'))
    print(dict_top([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 1, 'b': 3}, {'a': 2, 'b': 4}], 'a', 2, reverse=True))
    print(dict_flatten({'a': 1, 'b': 'b', 'c': [1, 2], 'd': {'a': 1, 'b': 2}, 'e': [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]}))
    print(dict_format_type({'a': 1, 'b': 'b', 'c': [1, 2], 'd': {'a': 1, 'b': 2}, 'e': [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]}, int, lambda _i: _i + 1))
    print(dict_remove_key({'a': 1, 'b': 2}, 'a'))
    print(dict_remove_value({'a': 1, 'b': 2}, 2))
    print(dict_as_tuple_list({'a': 1, 'b': 2}))
    print(tuple_search([('a', 1), ('b', 2), ('a', 3), ('b', 4)], 1, 1))
    print(string_insert('apple', ' banana', 3))
    print(format_datetime(datetime.fromtimestamp(datetime.now().timestamp() + 3600 * 24)))
    print(format_date())
    print(format_time())

