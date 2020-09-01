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


