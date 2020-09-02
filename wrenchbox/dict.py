from .list import EnhancedList


class EnhancedDict:
    def __init__(self, d: dict):
        self.d = d.copy()

    def search(self, key, full=False, dive=True):
        """
        Search dict and find all items with certain keys
        :param key: key
        :param full: the entire dicts will be returned as results if set to true
        :param dive: continue searching even if key is already matched
        :return: list of items
        """
        result = []
        for k, v in self.d.items():
            if key == k:
                result.append(self.d if full else v)
            if dive:
                if isinstance(v, dict):
                    result += EnhancedDict(v).search(key, full, dive)
                elif isinstance(v, list):
                    result += EnhancedList(EnhancedList(v).format(lambda x: EnhancedDict(x).search(key, full, dive) if isinstance(x, dict) else None)).flatten()
        return result

    def merge(self, d: dict):
        """
        Merge another dict into this dict
        :param d: the other dict
        :return: the merged dict (self.d)
        """
        for k in d:
            if k in self.d and isinstance(self.d[k], dict) and isinstance(d[k], dict):
                self.d[k] = EnhancedDict(self.d[k]).merge(d[k])
            else:
                self.d[k] = d[k]
        return self.d

    def flatten(self):
        """
        Replace nested dict keys to underscore-connected keys
        :return: flattened dictionary
        """
        result = dict()
        for k, v in self.d.items():
            if isinstance(v, dict):
                for kk, vv in EnhancedDict(v).flatten().items():
                    result[k + '_' + kk] = vv
            else:
                result[k] = v
        return result

    def format(self, formatter, picker=None):
        """
        Format the values of the dict
        :param formatter: formatter method, e.g., return the string format of an int
        :param picker: picker method, e.g., return not none
        :return: formatted dictionary (self.d)
        """
        for k in self.d.keys():
            if isinstance(self.d[k], list):
                self.d[k] = EnhancedList(self.d[k]).format(
                    lambda x: EnhancedDict(x).format(formatter, picker) if isinstance(x, dict) else (
                        formatter(x) if picker is None or (picker is not None and picker(x)) else x
                    )
                )
            elif isinstance(self.d[k], dict):
                self.d[k] = EnhancedDict(self.d[k]).format(formatter, picker)
            elif picker is None or (picker is not None and picker(self.d[k])):
                self.d[k] = formatter(self.d[k])
        return self.d

    # def dict_remove_key(d, k):
    #     """
    #     Recursively remove a key from a dict
    #     :param d: the dictionary
    #     :param k: key which should be removed
    #     :return: formatted dictionary
    #     """
    #     if isinstance(d, dict):
    #         dd = dict()
    #         for key, value in d.items():
    #             if not key == k:
    #                 dd[key] = dict_remove_key(value, k)
    #         return dd
    #     elif isinstance(d, list):
    #         return [dict_remove_key(i, k) for i in d]
    #     else:
    #         return d
    #
    # def dict_remove_value(d, v):
    #     """
    #     Recursively remove keys with a certain value from a dict
    #     :param d: the dictionary
    #     :param v: value which should be removed
    #     :return: formatted dictionary
    #     """
    #     dd = dict()
    #     for key, value in d.items():
    #         if not value == v:
    #             if isinstance(value, dict):
    #                 dd[key] = dict_remove_value(value, v)
    #             elif isinstance(value, list):
    #                 dd[key] = [dict_remove_value(i, v) for i in value]
    #             else:
    #                 dd[key] = value
    #     return dd
    #
    # def dict_as_tuple_list(d, as_list=False):
    #     """
    #     Format a dict to a list of tuples
    #     :param d: the dictionary
    #     :param as_list: return a list of lists rather than a list of tuples
    #     :return: formatted dictionary list
    #     """
    #     dd = list()
    #     for k, v in d.items():
    #         dd.append([k, v] if as_list else (k, v))
    #     return dd


# class EnhancedDictList:
#     def __init__(self, m: list):
#         self.d = d
#
#     def search_by_key_value(self, key, value):
#         """
#         Search dictionary list by key and value
#         :param d: dictionary list
#         :param k: key
#         :param v: value
#         :return: the index of the first dictionary in the array with the specific key / value
#         """
#         for i in range(len(d)):
#             if d[i][k] == v:
#                 return i
#         return None
#
#     def dict_sort(d, k):
#         """
#         Sort a dictionary list by key
#         :param d: dictionary list
#         :param k: key
#         :return: sorted dictionary list
#         """
#         return sorted(d.copy(), key=lambda i: i[k])
#
#     def dict_top(d, k, n, reverse=False):
#         """
#         Return top n of a dictionary list sorted by key
#         :param d: dictionary list
#         :param k: key
#         :param n: top n
#         :param reverse: whether the value should be reversed
#         :return: top n of the sorted dictionary list
#         """
#         h = list()
#         for i in range(len(d)):
#             heappush(h, (-d[i][k] if reverse else d[i][k], i))
#         r = list()
#         while len(r) < n and len(h) > 0:
#             _, i = heappop(h)
#             r.append(d[i].copy())
#         return r
#
#     def tuple_search(t, i, v):
#         """
#         Search tuple array by index and value
#         :param t: tuple array
#         :param i: index of the value in each tuple
#         :param v: value
#         :return: the first tuple in the array with the specific index / value
#         """
#         for e in t:
#             if e[i] == v:
#                 return e
#         return None


if __name__ == "__main__":
    dict_a = {
        'a': 1,
        'b': {
            'a': 1,
            'b': {
                'a': 1,
                'b': [{
                    'a': 1,
                    'b': 2
                }, {
                    'a': 1,
                    'b': {
                        'a': 1,
                        'b': 2
                    }
                }]
            }
        }
    }
    dict_b = {
        'a': 1,
        'b': {
            'b': {
                'b': 2
            }
        }
    }
    print(dict_a)
    print(dict_b)
    print(EnhancedDict(dict_a).search('a'))
    print(EnhancedDict(dict_a).merge(dict_b))
    print(EnhancedDict(dict_b).flatten())
    print(EnhancedDict(dict_a).format(lambda x: x + 10, lambda x: x == 1))
