#!/usr/bin/env python3
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.logUtils import logger


class ApiRun:

    def api_get_code(self, url):
        logger.info("获取验证码url,{}".format(url))
        return requests.get(url)
    

    #通用请求
    def api_requests(self, url=None, method=None, headers=None, data=None, cookies=None):
        logger.info("请求的url为：{}".format(url))
        logger.info("请求的方式为：{}".format(method))
        if headers:
            logger.info("请求的headers为：{}".format(headers))
        if cookies:
            logger.info("携带的cookie为：{}".format(cookies))
        if data:
            logger.info("请求数据：{}".format(data))
        try:
            res = requests.request(url=url, method=method, headers=headers, data=data, cookies=cookies)
            assert res.status_code == 200
            return res
        except Exception as e:
            logger("用例执行出错，请查看日志定位问题：{}".format(e))
            assert False