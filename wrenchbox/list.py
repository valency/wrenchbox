class EnhancedList:
    def __init__(self, r: list):
        self.r = r.copy()

    def flatten(self):
        result = []
        for i in self.r:
            if isinstance(i, list):
                result += EnhancedList(i).flatten()
            else:
                result.append(i)
        return result

    def pick(self, picker, reverse=False):
        result = []
        for i in self.r:
            if isinstance(i, list):
                candidates = EnhancedList(i).pick(picker, reverse)
                if candidates:
                    result.append(candidates)
            else:
                if picker(i) ^ reverse:
                    result.append(i)
        return result

    def format(self, formatter, picker=None):
        for i in range(len(self.r)):
            if isinstance(self.r[i], list):
                self.r[i] = EnhancedList(self.r[i]).format(formatter, picker)
            elif picker is not None and picker(self.r[i]):
                self.r[i] = formatter(self.r[i])
        return self.r


if __name__ == "__main__":
    list_a = [1, [1, [2, 3], 2], 2]
    print(list_a)
    print(EnhancedList(list_a).flatten())
    print(EnhancedList(list_a).pick(lambda x: x == 1))
    print(EnhancedList(list_a).pick(lambda x: x == 1, reverse=True))
    print(EnhancedList(list_a).format(lambda x: x + 1, lambda x: isinstance(x, (int, float))))
