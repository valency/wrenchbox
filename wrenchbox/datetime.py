from datetime import datetime

from dateutil import parser


class T:
    def __init__(self, t=None):
        if t is not None:
            if isinstance(t, int) or isinstance(t, float):
                self.t = datetime.fromtimestamp(t)
            elif isinstance(t, datetime):
                self.t = t
            elif isinstance(t, str):
                try:
                    self.t = datetime.fromtimestamp(int(t))
                except ValueError:
                    try:
                        self.t = datetime.fromtimestamp(float(t))
                    except ValueError:
                        self.t = parser.parse(t)
            else:
                raise ValueError
        else:
            self.t = datetime.now()

    def timestamp(self):
        """
        Get the timestamp of the datetime object
        :return: timestamp
        """
        return self.t.timestamp()

    def format(self, m: str = 'dt'):
        """
        Format the datetime object into various forms
        :param m: format, 'dt' or 'd' or 't'
        :return: the formatted string
        """
        if m == 'dt':
            return self.t.strftime('%Y-%m-%d %H:%M:%S')
        elif m == 'd':
            return self.t.strftime('%Y-%m-%d')
        elif m == 't':
            return self.t.strftime('%H:%M:%S')


if __name__ == "__main__":
    print(T().timestamp())
    print(T().format())
    print(T().format('d'))
    print(T().format('t'))
