import argparse
import logging
import re

from jieba import posseg

from .logging import setup_log


class S:
    def __init__(self, s):
        self.s = s
        self.words = None

    def v(self, chinese=False):
        if chinese:
            words = list()
            for w, a in posseg.cut(self.s):
                words.append((w, a))
        else:
            words = [(w, None) for w in re.sub("[^\w]", " ", self.s).split()]
        self.words = list()
        for w in set(words):
            self.words.append((w[0], w[1], words.count(w)))
        self.words = sorted(self.words, key=lambda x: x[2])
        self.words.reverse()
        return self


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False, help='show debug information')
    parser.add_argument('--chinese', action='store_true', default=False, help='specify the input as Chinese')
    parser.add_argument('-p', type=str, default=None, help='part of speech to show, only works for Chinese')
    parser.add_argument('f', type=str, help='file path')
    args, _ = parser.parse_known_args()
    setup_log(level=logging.DEBUG if args.debug else logging.INFO)
    print([i for i in S(open(args.f, 'r').read()).v(chinese=args.chinese).words if i[1] in [i.strip() for i in args.p.split(',')]])
