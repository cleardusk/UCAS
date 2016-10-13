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
            message = u'success'
            return message
        return u'false, may already online'

    def _operation(self, method):
        url = 'http://210.77.16.21/eportal/InterFace.do?method={}'.format(
            method)
        if method in ['login']:
            r = self.session.get('http://210.77.16.21/')
            query_string = r.url[r.url.find('wlan'):]
            data = {'userId': self.user_id,
                    'password': self.password,
                    'queryString': query_string,
                    'service': '',
                    'operatorPwd': '',
                    'validcode': ''}
            self.session.post(url=url, data=data)

            # the response is string in json format
            # use `decode('utf-8')' is for compatibility in python3, python2
            # works too
        else:
            print('method {} is NOT supported'.format(method))

    def login_ucas(self):
        self._operation('login')

    # china unicom login
    def login_cu(self):
        url = 'http://202.106.46.37/login.do?username={}&password={}' \
              '&passwordType=6&userOpenAddress=bj&checkbox=0'.format(
                  self.user_id, self.password)

        self.session.get(url)


def login(fp, option='ucas'):
    info = json.load(open(fp))
    app = Ucas(user_id=info.get('user_id'), password=info.get('password'))
    if option == 'ucas':
        app.login_ucas()
    elif option == 'unicom':
        app.login_cu()


def logout(option='ucas'):
    app = Ucas()
    if option == 'ucas':
        app.logout_ucas()
    elif option == 'unicom':
        app.logout_cu()


def make_abs_path(fl):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), fl)

if __name__ == '__main__':
    # main()
    login(make_abs_path('config.json'), 'ucas')
    #login(make_abs_path('config_cu.json'), 'cu')
