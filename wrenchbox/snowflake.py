import argparse
import logging
import time

from .logging import setup_log


class Snowflake:
    def __init__(self, twepoch):
        """
        Init a snowflake generator: https://developer.twitter.com/en/docs/twitter-ids
        :param twepoch: an initial timestamp when the database is created, e.g., 1483228800000
        """
        self.twepoch = twepoch
        self.worker_id_bits = 5
        self.data_center_id_bits = 5
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.max_data_center_id = -1 ^ (-1 << self.data_center_id_bits)
        self.sequence_bits = 12
        self.worker_id_shift = self.sequence_bits
        self.data_center_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_left_shift = self.sequence_bits + self.worker_id_bits + self.data_center_id_bits
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)

    def timestamp(self, k):
        """
        Return the timestamp of a snowflake code
        :param k: the snowflake code
        :return: timestamp of the snowflake code
        """
        s = k >> 22
        s += self.twepoch
        return s / 1000

    def generate(self, worker_id, data_center_id=31, sleep=lambda x: time.sleep(x / 1000.0), count=1):
        """
        Generate a snowflake code
        :param worker_id: worker id, 0-31
        :param data_center_id: data center id, 0-31
        :param sleep: sleep time after one batch of codes are generated
        :param count: # of desired codes
        :return: a list of snowflake codes
        """
        assert 0 <= worker_id <= self.max_worker_id
        assert 0 <= data_center_id <= self.max_data_center_id
        last_timestamp = -1
        sequence = 0
        c = 0
        while c < count:
            timestamp = int(time.time() * 1000)
            if last_timestamp > timestamp:
                logging.warning("Clock is moving backwards, wait until: {}".format(last_timestamp))
                sleep(last_timestamp - timestamp)
                continue
            if last_timestamp == timestamp:
                sequence = (sequence + 1) & self.sequence_mask
                if sequence == 0:
                    logging.warning("Sequence overruns.")
                    sequence = -1 & self.sequence_mask
                    sleep(1)
                    continue
            else:
                sequence = 0
            last_timestamp = timestamp
            c += 1
            yield ((timestamp - self.twepoch) << self.timestamp_left_shift) | (data_center_id << self.data_center_id_shift) | (worker_id << self.worker_id_shift) | sequence


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False, help='show debug information')
    parser.add_argument('--twepoch', type=int, default=1483228800000, help='twitter epoch, default: 1483228800000')
    parser.add_argument('-d', type=int, default=31, help='data center id, default: 31')
    parser.add_argument('-w', type=int, required=True, help='worker id, 0-31')
    parser.add_argument('n', type=int, help='# of results')
    args, _ = parser.parse_known_args()
    setup_log(level=logging.DEBUG if args.debug else logging.INFO)
    [print(i) for i in Snowflake(twepoch=args.twepoch).generate(args.w, data_center_id=args.d, count=args.n)]
