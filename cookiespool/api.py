# coding=utf-8
import json
from flask import Flask, g
from cookiespool.config import *
from cookiespool.db import *

'''
[接口模块]
'''


__all__ = ['app']
app = Flask(__name__)


@app.route('/')
def index():
    '''
    web接口首页
    :return:
    '''
    return '<h2>Welcome to Cookie Pool System</h2>'


def get_conn():
    """
    使用flask特性/ 注意方法->hasattr/ setattr/ getattr
    :return:
    """
    for website in GENERATOR_MAP:
        print('website->', website)
        # attention +--
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts", "' + website + '")'))
        # -------------
    return g


@app.route('/<website>/random')
def random(website):
    """
    获取随机的Cookie, 访问地址如 /weibo/random
    :return: 随机Cookie
    """
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies


@app.route('/<website>/add/<username>/<password>')
def add(website, username, password):
    """
    添加用户, 访问地址如 /weibo/add/user/password
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return: 
    """
    g = get_conn()
    print(username, password)
    getattr(g, website + '_accounts').set(username, password)
    return json.dumps({'status': '1'})


@app.route('/<website>/count')
def count(website):
    """
    获取Cookies总数
    """
    g = get_conn()
    count = getattr(g, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
