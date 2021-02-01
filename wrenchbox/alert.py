import argparse
import logging

import requests

from .logging import setup_log


class DingTalk:
    base_url = 'https://oapi.dingtalk.com/robot/'

    def __init__(self, access_token):
        self.access_token = access_token

    def send(self, msg, msg_type='text', title='ERROR'):
        m = {
            'msgtype': msg_type
        }
        if msg_type == 'text':
            m['text'] = {
                'content': msg
            }
        elif msg_type == 'markdown':
            m['markdown'] = {
                'title': title,
                'text': msg
            }
        else:
            raise ValueError('unknown msg type: {}'.format(msg_type))
        return requests.post('{}send?access_token={}'.format(self.base_url, self.access_token), json=m)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False, help='show debug information')
    parser.add_argument('--type', '-p', type=str, required=True, help='alert type, must be "dingtalk"')
    parser.add_argument('--token', '-k', type=str, default=None, help='access token, if any')
    parser.add_argument('msg', type=str, help='the message')
    args, _ = parser.parse_known_args()
    setup_log(level=logging.DEBUG if args.debug else logging.INFO)
    print({'dingtalk': DingTalk}[args.type](args.token).send(args.msg).text)
