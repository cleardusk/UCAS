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

    def login_ucas(self):
        self._operation('login')

    def logout_ucas(self):
        self._operation('logout')

    def info(self):
        self._operation('getOnlineUserInfo')

    # china unicom login
    def login_cu(self):
        url = 'http://202.106.46.37/login.do?username={}&password={}' \
              '&passwordType=6&userOpenAddress=bj&checkbox=0'.format(self.user_id, self.password)

        r = self.session.get(url).content.decode('utf-8')
        # r = re.findall('"message":"([a-z]+)"', r)[0]
        pos = r.find('message')
        r = r[pos + 10:]
        pos = r.find('"')
        message = r[:pos]
        if message == 'success':
            print(u'登陆成功（联通）！')
        else:
            print(message)

    # china unicom logout
    def logout_cu(self):
        url = 'http://202.106.46.37/logout.do'
        try:
            self.session.get(url, timeout=4)
            print(u'退出成功（联通）！')
        except:
            print(u'退出出错（联通）！检查下之前用户是否在线？')


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


def main():
    parser = argparse.ArgumentParser(description='ucas utils')
    parser.add_argument('-D', '--do', type=str, default='login')
    parser.add_argument('-O', '--option', type=str, default='ucas')
    parser.add_argument('-C', '--config', type=str, default='config.json')
    args = parser.parse_args()

    if args.do.lower() in ['login', 'online', 'on']:
        # get the absolute path of config file
        fp = make_abs_path(args.config)
        if args.option.lower() in ['ucas']:
            login(fp, 'ucas')
        elif args.option.lower() in ['unicom', 'cu']:
            login(fp, 'unicom')
    elif args.do.lower() in ['logout', 'offline', 'off']:
        if args.option.lower() in ['ucas']:
            logout('ucas')
        elif args.option.lower() in ['unicom', 'cu']:
            logout('unicom')


if __name__ == '__main__':
    main()
