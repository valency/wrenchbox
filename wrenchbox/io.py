import gzip
import logging
import os
import time
from datetime import datetime

from .logging import setup_log


class BufferedWriter:
    def __init__(self, path='.', prefix='', buffer=100000):
        """
        Buffered writer
        :param path: writing path where files will be stored as <timestamp>.dat.gz
        :param prefix: prefix for all files
        :param buffer: the buffer size
        """
        self.data = list()
        self.path = path
        self.prefix = prefix
        self.buffer = buffer

    def write(self, data):
        """
        Write data to file
        :param data: one line of data
        :return: none
        """
        self.data.append(data)
        if len(self.data) >= self.buffer:
            self.out()

    def out(self):
        """
        Immediately write all buffers to file
        :return: none
        """
        if len(self.data):
            batch = self.data[:self.buffer]
            self.data = self.data[self.buffer:]
            logging.info('Writing out {} records...'.format(len(batch)))
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            with gzip.open(os.path.join(self.path, '{}{}.dat.gz'.format(self.prefix, int(datetime.now().timestamp()))), 'wb') as f:
                for i in batch:
                    f.write((str(i) + '\n').encode('utf-8'))

    def close(self):
        """
        Close the writer and write remaining buffer to file
        :return: none
        """
        self.out()


if __name__ == "__main__":
    setup_log()
    _w = BufferedWriter(buffer=50)
    for _i in range(100):
        _w.write(_i)
        time.sleep(0.02)
    _w.close()
