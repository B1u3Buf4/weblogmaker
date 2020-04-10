#!/usr/bin python3
# -*- coding: utf-8 -*-

import faker
import time
import random
import argparse


methods = {'GET': 10, 'POST':4, 'PUT':1, 'HEAD':2, 'OPTIONS':1, 'DELETE':1, 'TRACE':1, 'CONNECT':1}
status_codes = {200: 10, 301:1, 302:3, 403:1, 404:1}

def fake_weblog_std(methods, status_codes):
    f = faker.Faker()
    me = []
    for k, v in methods.items():
        me.extend([k for i in range(v)])
    code = []
    for k, v in status_codes.items():
        code.extend([k for i in range(v)])
    method = me[random.randint(0, len(me) - 1)]
    status_code = code[random.randint(0, len(code) - 1)]
    if method == 'HEAD':
        length = 0
    else:
        length = random.randint(0, 10000)
    return f'{f.ipv4_public()} - - [{time.strftime("%d/%b/%Y:%H:%M:%S", time.localtime(time.time()))} +0800] "{method} /{f.uri_path()}{f.uri_extension()} HTTP/1.1" {str(status_code)} {str(length)}\n'


def fake_weblog_ext(methods, status_codes):
    f = faker.Faker()
    me = []
    for k, v in methods.items():
        me.extend([k for i in range(v)])
    code = []
    for k, v in status_codes.items():
        code.extend([k for i in range(v)])
    method = me[random.randint(0, len(me) - 1)]
    status_code = code[random.randint(0, len(code) - 1)]
    ua = f.user_agent()
    if method == 'HEAD':
        length = 0
    else:
        length = random.randint(0, 10000)
    return f'{f.ipv4_public()} - - [{time.strftime("%d/%b/%Y:%H:%M:%S", time.localtime(time.time()))} +0800] "{method} /{f.uri_path()+f.uri_extension()} HTTP/1.1" {str(status_code)} {str(length)} {f.url()+f.uri_path()+f.uri_extension()} {ua}\n'


def _dic2list(input_dic):
    result = []
    if isinstance(input_dic, dict):
        for k, v in input_dic.items():
            if isinstance(v, int):
                result.extend([k for i in range(v)])
    return result


def main(args):
    with open(args.o, 'w') as f:
        for i in range(int(args.c)):
            if args.e:
                f.write(fake_weblog_ext(args.m, args.s))
            else:
                f.write(fake_weblog_std(args.m, args.s))


if __name__ == '__main__':
    """
    -e 缺失生成标准日志，存在则生成扩展日志。
    -c 生成日志的数量。
    -o 导出目录路径。
    -m 输入请求方法计数字典。
    -s 输入状态码计数字典。
    """
    parser = argparse.ArgumentParser(usage="Make web middleware log.", description="Two log style: std(default) or ext(with UA and referer).")
    parser.add_argument("-e", help="Use extended log style.", action="store_true")
    parser.add_argument("-c", default=1, help="Log count.")
    parser.add_argument("-o", default='./result.log', help="Output path.")
    parser.add_argument("-m", default=methods, help="HTTP request method dict with counter. e.g. {'GET':10, 'POST:3'}")
    parser.add_argument("-s", default=status_codes, help="HTTP request method dict with counter. e.g. {200:10, 302:1, 403:1}")
    args = parser.parse_args()
    main(args)
