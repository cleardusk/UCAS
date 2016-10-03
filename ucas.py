#!/usr/bin/env python
# coding: utf-8

import requests
import json
import argparse
import os


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
            r = json.loads(r.content.decode('utf-8'))
            print(self.parse_res(r))
        elif method in ['getOnlineUserInfo']:
            r = self.session.post(url=url)
            print(r.content.decode('utf-8'))
        else:
            print('method {} is NOT supported'.format(method))

    def login(self):
        self._operation('login')

    def logout(self):
        self._operation('logout')

    def info(self):
        self._operation('getOnlineUserInfo')


def main():
    parser = argparse.ArgumentParser(description='ucas utils')
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
