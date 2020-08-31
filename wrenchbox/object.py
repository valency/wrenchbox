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
