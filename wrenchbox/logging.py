import logging
import os
import sys
import time
from datetime import datetime

from django.utils.termcolors import colorize


class Formatter(logging.Formatter):
    color = {
        logging.DEBUG: 'cyan',
        logging.INFO: 'green',
        logging.WARNING: 'yellow',
        logging.ERROR: 'red',
        logging.CRITICAL: 'magenta',
    }

    def format(self, record):
        original = self._style._fmt
        self._style._fmt = colorize('[%(asctime)s] ', fg=self.color[record.levelno]) + '%(message)s'
        result = logging.Formatter.format(self, record)
        self._style._fmt = original
        return result


def setup_log(level=logging.INFO, path=None, tag: str = None):
    """
    Setup logging with color formats
    :param level: logging level via logging.INFO / logging.WARNING / logging.ERROR, etc.
    :param path: logs will be written to a file instead of stdout if provided
    :param tag: a prefix of the log file if path if provided
    :return: none
    """
    # Stream handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(Formatter())
    logging.root.addHandler(handler)
    # File handler
    if path is not None:
        if not os.path.exists(path):
            os.makedirs(path)
        handler = logging.FileHandler("{}/{}{}.log".format(path, tag + '-' if tag is not None else '', datetime.utcnow().timestamp()), encoding='utf-8')
        handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
        logging.root.addHandler(handler)
    # Set logging level
    logging.root.setLevel(level)


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
    setup_log(level=logging.DEBUG, path='./log/', tag='wrenchbox')
    logging.debug('This is a DEBUG message.')
    logging.info('This is an INFO message.')
    logging.warning('This is a WARNING message.')
    logging.error('This is an ERROR message.')
    logging.critical('This is an CRITICAL message.')
    for _i in range(100):
        progress(_i, 100)
        time.sleep(0.02)
