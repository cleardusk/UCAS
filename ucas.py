#!/usr/bin/env python
# coding: utf-8

import requests
import json
import random
import argparse
import os

LOGIN_HAS_FLOW = 0
LOGIN_NO_FLOW = 1
LOGIN_FAIL = 2  # user not exists, password wrong and so on.


class Ucas:
    def __init__(self, **info):
        self.session = requests.session()
        self.user_id = info.get('user_id')
        self.password = info.get('password')

    def parse_res(self, r):
        result = r.get('result')
        message = r.get('message')
        if not message:
            message = u'登陆成功！'
        # if self.user_id is None:
        #     return u'{}, {}'.format(result, message)
        # else:
        #     return u'{}: {}, {}'.format(self.user_id, result, message)
        return u'{}: {}'.format(result, message)

    def _operation(self, method):
        url = 'http://210.77.16.21/eportal/InterFace.do?method={}'.format(method)
        if method in ['login']:
            r = self.session.get('http://210.77.16.21/')
            query_string = r.url[r.url.find('wlan'):]
            data = {'userId': self.user_id,
                    'password': self.password,
                    'queryString': query_string,
                    'service': '',
                    'operatorPwd': '',
                    'validcode': ''}
            r = self.session.post(url=url, data=data)

            # the response is string in json format
            # use `decode('utf-8')' is for compatibility in python3, python2 works too
            r = json.loads(r.content.decode('utf-8'))

            print(self.parse_res(r))
            if r.get('result') in ['success'] or r.get('message') in [u'无可用剩余流量']:
                return True
            return False
        elif method in ['logout']:
            r = self.session.post(url=url)
            r = json.loads(r.content)
            print(self.parse_res(r))
        elif method in ['getOnlineUserInfo']:
            r = self.session.post(url=url)
            print(r.content)
            # r = json.loads(r.content)
            # json.dump(r, open('info.json', 'w'),indent=True)
            # print(json.dumps(r, indent=True))
            # print(r)
        else:
            print('method {} is NOT supported'.format(method))

    def login(self):
        self._operation('login')

    def logout(self):
        self._operation('logout')

    def info(self):
        self._operation('getOnlineUserInfo')


def test_valid():
    user_ids = json.load(open('user_ids.json'))
    valid = {}
    for user_id, user_name in user_ids.iteritems():
        ucas = Ucas(user_id=user_id, password='ucas')
        if ucas.login():
            ucas.logout()
            valid[user_id] = user_name

    json.dump(valid, open('user_ids2.json', 'w'), indent=True)


def main():
    parser = argparse.ArgumentParser(description='ucas tools')
    parser.add_argument('-D', '--do', type=str, default='login')
    args = parser.parse_args()

    if args.do.lower() in ['login', 'online', 'on']:
        # get the absolute path of config file
        fp = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')
        info = json.load(open(fp))
        Ucas(user_id=info.get('user_id'), password=info.get('password')).login()
    elif args.do.lower() in ['logout', 'offline', 'off']:
        Ucas().logout()


if __name__ == '__main__':
    main()
    # test_valid()
