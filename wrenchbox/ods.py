import argparse
import json
import logging

import requests
from deeputils.common import Dict2StrSafe
from deeputils.logger import setup_log
from qiniu import Auth


class Qiniu(Dict2StrSafe):
    def __init__(self, access_key: str, secret_key: str, domain: str, bucket: str = None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.domain = domain
        self.bucket = bucket
        self.q = Auth(self.access_key, self.secret_key)

    def get(self, item: str):
        url = self.q.private_download_url('http://{}/{}'.format(self.domain, item), expires=3600)
        r = requests.get(url)
        r.encoding = 'utf-8'
        return r.json()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False, help='show debug information')
    parser.add_argument('-k', type=str, required=True, help='access key')
    parser.add_argument('-s', type=str, required=True, help='secret key')
    parser.add_argument('-d', type=str, required=True, help='domain')
    parser.add_argument('-b', type=str, default=None, help='bucket (optional)')
    parser.add_argument('-e', action='store_true', help='extract all "$id" values')
    parser.add_argument('id', type=str, help='object ID')
    args, _ = parser.parse_known_args()
    setup_log(level=logging.DEBUG if args.debug else logging.INFO)
    if args.e:
        print(json.dumps(Qiniu.extract(Qiniu(args.k, args.s, args.d, args.b).get(args.id), '$id'), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(Qiniu(args.k, args.s, args.d, args.b).get(args.id), indent=2, ensure_ascii=False))
