import json


class Dict2StrSafe:
    # A class that correctly converts self.__dict__ to json string without errors
    def __str__(self):
        s = dict()
        for k, v in self.__dict__.items():
            if isinstance(v, list):
                s[k] = [json.loads(str(i)) if isinstance(i, Dict2StrSafe) else i for i in v]
            elif isinstance(v, Dict2StrSafe):
                s[k] = json.loads(str(v))
            else:
                s[k] = v
        return json.dumps(s, default=lambda i: str(i))


class Munch(Dict2StrSafe):
    def __init__(self, m: dict = None, **kwargs):
        """
        An alternative implementation of munch
        :param m: a dict
        """
        if m:
            for k, v in m.items():
                if isinstance(v, dict):
                    setattr(self, k, Munch(v))
                else:
                    setattr(self, k, v)
        for k, v in kwargs.items():
            if isinstance(v, dict):
                setattr(self, k, Munch(v))
            else:
                setattr(self, k, v)


if __name__ == '__main__':
    print(json.dumps(json.loads(str(Munch({'a': 1, 'b': {'a': 1, 'b': 2}}, a=3, c=1))), indent=2))
