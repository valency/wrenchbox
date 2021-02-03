import argparse
import logging
import random
import threading
import time
import uuid

from .logging import setup_log


class Master:
    def __init__(self, max_threads=10):
        self.max_threads = max_threads
        self.threads = []

    def run(self, target, target_args):
        while True:
            while len(self.threads) < self.max_threads:
                thread = threading.Thread(target=target, args=target_args)
                logging.info('New thread is spawned: %s', thread.name)
                thread.start()
                self.threads.append(thread)
            threads = []
            for thread in self.threads:
                if thread.is_alive():
                    threads.append(thread)
                else:
                    logging.info('Thread is terminated: %s', thread.name)
            self.threads = threads


def test():
    x = random.randint(1, 30)
    n = uuid.uuid4()
    logging.info('Sleeping %s seconds: %s', x, n)
    time.sleep(x)
    logging.info('Sleeping is completed: %s', n)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False, help='show debug information')
    args, _ = parser.parse_known_args()
    setup_log(level=logging.DEBUG if args.debug else logging.INFO)
    Master().run(test, ())
