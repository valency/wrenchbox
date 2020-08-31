import json
import random
import string
import sys
import time
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_DOWN
from heapq import heappush, heappop
from math import pi





def decimal_safe(i):
    """
    Returns the decimal format of a given number
    :param i: the number
    :return: the decimal format of the number
    """
    if i is None:
        return None
    elif not isinstance(i, Decimal):
        try:
            return Decimal(repr(i))
        except InvalidOperation:
            return Decimal(i)
    else:
        return i


def decimal_round(i, r=None, d=ROUND_HALF_DOWN):
    """
    Round a decimal number with a given unit
    :param i: the decimal number
    :param r: the unit, e.g., 1, 0.5
    :param d: rounding direction, see decimal.ROUND_* for details
    :return: the rounded number
    """
    if i is not None:
        i = decimal_safe(i)
        if r is not None:
            r = decimal_safe(r)
            return (i / r).to_integral_exact(rounding=d) * r
        else:
            return i
    else:
        return None


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




def tuple_search(t, i, v):
    """
    Search tuple array by index and value
    :param t: tuple array
    :param i: index of the value in each tuple
    :param v: value
    :return: the first tuple in the array with the specific index / value
    """
    for e in t:
        if e[i] == v:
            return e
    return None


def string_insert(str1, str2, i):
    """
    Insert a string in the middle of another string
    :param str1: the original string
    :param str2: the string to be inserted
    :param i: the index of the insertion position
    :return: the resulting string
    """
    return str1[:i] + str2 + str1[i:]


def format_datetime(t: datetime = None):
    """
    Format a datetime object into yyyy-MM-dd hh:mm:ss
    :param t: datetime object, default: now
    :return: the formatted string
    """
    return (datetime.now() if t is None else t).strftime('%Y-%m-%d %H:%M:%S')


def format_date(t: datetime = None):
    """
    Format a datetime object into yyyy-MM-dd
    :param t: datetime object, default: now
    :return: the formatted string
    """
    return (datetime.now() if t is None else t).strftime('%Y-%m-%d')


def format_time(t: datetime = None):
    """
    Format a datetime object into hh:mm:ss
    :param t: datetime object, default: now
    :return: the formatted string
    """
    return (datetime.now() if t is None else t).strftime('%H:%M:%S')


def progress(count, total, prefix='', suffix='', length=60):
    """
    Show a progress bar
    :param count: current progress
    :param total: total progress
    :param prefix: prefix shown before the progress bar
    :param suffix: suffix shown after the progress bar
    :param length: length of the progress bar, default: 60
    :return: none
    """
    bar_len = length
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('%s[%s] %s%s%s\r' % (prefix, bar, percents, '%', ' ' + suffix))
    sys.stdout.flush()


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
    for _i in range(100):
        progress(_i, 100)
        time.sleep(0.02)
