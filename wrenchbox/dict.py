import time
from datetime import datetime
from heapq import heappush, heappop
from math import pi


class EnhancedDict:
    def __init__(self, d: dict):
        self.d = d

    def search_by_key(self, key, dive=True):
        """
        Search dict and find all items with certain keys
        :param key: key
        :param dive: continue searching even if key is already matched
        :return: list of items
        """
        results = []
        for k, v in self.d.items():
            if key == k:
                results.append(v)
            if dive:
                if isinstance(v, dict):
                    results += EnhancedDict(v).search_by_key(key, dive)
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            results += EnhancedDict(item).search_by_key(key, dive)
        return results



    def dict_merge(a, b, k):
        """
        Merge two dictionary lists
        :param a: original list
        :param b: alternative list, element will replace the one in original list with same key
        :param k: key
        :return: the merged list
        """
        c = a.copy()
        for j in range(len(b)):
            flag = False
            for i in range(len(c)):
                if c[i][k] == b[j][k]:
                    c[i] = b[j].copy()
                    flag = True
            if not flag:
                c.append(b[j].copy())
        return c

    def dict_sort(d, k):
        """
        Sort a dictionary list by key
        :param d: dictionary list
        :param k: key
        :return: sorted dictionary list
        """
        return sorted(d.copy(), key=lambda i: i[k])

    def dict_top(d, k, n, reverse=False):
        """
        Return top n of a dictionary list sorted by key
        :param d: dictionary list
        :param k: key
        :param n: top n
        :param reverse: whether the value should be reversed
        :return: top n of the sorted dictionary list
        """
        h = list()
        for i in range(len(d)):
            heappush(h, (-d[i][k] if reverse else d[i][k], i))
        r = list()
        while len(r) < n and len(h) > 0:
            _, i = heappop(h)
            r.append(d[i].copy())
        return r

    def dict_flatten(d):
        """
        Replace nested dict keys to underscore-connected keys
        :param d: the dictionary
        :return: flattened dictionary
        """
        if type(d) != dict:
            return d
        else:
            dd = dict()
            for key, value in d.items():
                if type(value) == dict:
                    for k, v in value.items():
                        dd[key + '_' + k] = dict_flatten(v)
                else:
                    dd[key] = value
            return dd

    def dict_format_type(d, source, formatter, include_list=True):
        """
        Replace the values of a dict with certain type to other values
        :param d: the dictionary
        :param source: the source type, e.g., int
        :param formatter: the formatter method, e.g., return the string format of an int
        :param include_list: whether list should be formatted, otherwise list will be considered as source type
        :return: formatted dictionary
        """
        if not isinstance(d, dict):
            if isinstance(d, source):
                return formatter(d)
            else:
                return d
        else:
            dd = dict()
            for key, value in d.items():
                if include_list and isinstance(value, list):
                    dd[key] = [dict_format_type(i, source, formatter) for i in value]
                elif isinstance(value, dict):
                    dd[key] = dict_format_type(value, source, formatter)
                elif isinstance(value, source):
                    dd[key] = formatter(value)
                else:
                    dd[key] = value
            return dd

    def dict_remove_key(d, k):
        """
        Recursively remove a key from a dict
        :param d: the dictionary
        :param k: key which should be removed
        :return: formatted dictionary
        """
        if isinstance(d, dict):
            dd = dict()
            for key, value in d.items():
                if not key == k:
                    dd[key] = dict_remove_key(value, k)
            return dd
        elif isinstance(d, list):
            return [dict_remove_key(i, k) for i in d]
        else:
            return d

    def dict_remove_value(d, v):
        """
        Recursively remove keys with a certain value from a dict
        :param d: the dictionary
        :param v: value which should be removed
        :return: formatted dictionary
        """
        dd = dict()
        for key, value in d.items():
            if not value == v:
                if isinstance(value, dict):
                    dd[key] = dict_remove_value(value, v)
                elif isinstance(value, list):
                    dd[key] = [dict_remove_value(i, v) for i in value]
                else:
                    dd[key] = value
        return dd

    def dict_as_tuple_list(d, as_list=False):
        """
        Format a dict to a list of tuples
        :param d: the dictionary
        :param as_list: return a list of lists rather than a list of tuples
        :return: formatted dictionary list
        """
        dd = list()
        for k, v in d.items():
            dd.append([k, v] if as_list else (k, v))
        return dd

class EnhancedDictList:
    def __init__(self, m: list):
        self.d = d

    def search_by_key_value(self, key, value):
        """
        Search dictionary list by key and value
        :param d: dictionary list
        :param k: key
        :param v: value
        :return: the index of the first dictionary in the array with the specific key / value
        """
        for i in range(len(d)):
            if d[i][k] == v:
                return i
        return None


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
