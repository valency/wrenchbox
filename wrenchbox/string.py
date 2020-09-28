import random
import string
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
    Generate a random string from [a-zA-Z0-9]
    :param n: length of the string
    :return: the random string
    """
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(n))


def random_letters(n):
    """
    Generate a random string from [a-zA-Z]
    :param n: length of the string
    :return: the random string
    """
    return ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(n))


def random_numbers(n):
    """
    Generate a random string from [0-9]
    :param n: length of the string
    :return: the random string
    """
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(n))


if __name__ == "__main__":
    print(digits(pi))
    print(random_chars(3))
    print(random_letters(3))
    print(random_numbers(3))
