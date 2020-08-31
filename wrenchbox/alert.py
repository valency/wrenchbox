import requests


class DingTalk:
    base_url = 'https://oapi.dingtalk.com/robot/'

    def __init__(self, access_token):
        self.access_token = access_token

    def send(self, msg):
        return requests.post('{}send?access_token={}'.format(self.base_url, self.access_token), json={
            'msgtype': 'text',
            'text': {
                'content': msg
            }
        })
