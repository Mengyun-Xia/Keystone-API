#!/usr/bin/env python3
import logging
import os
import time
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.settings import log_path


class LogUtil:
    def __init__(self):
        self.logger = logging.getLogger("logger")   #使用python自带的logging库封装日志
        self.logger.setLevel(logging.DEBUG)  #设定设置总的日志开关级别
        if not self.logger.handlers:  #避免日志重复
            self.log_name = '{}.log'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))) #定义日志名称
            self.log_path = os.path.join(log_path, self.log_name)  #定义日志路径及文件名称
            fh = logging.FileHandler(self.log_path, encoding='utf-8', mode='w')  #文件处理handler
            fh.setLevel(logging.DEBUG)  #文件处理handler的日志级别
            #日志内容格式
            formatter = logging.Formatter("%(asctime)s-%(filename)s[line%(lineno)d - %(levelname)s: %(message)s]")
            fh.setFormatter(formatter) #设置打印格式
            self.logger.addHandler(fh)  #添加hendler


    def log(self):
        return self.logger #返回定义好多的logger对象，对外直接用log函数即可
    

#其他程序可直接调用logger对象
logger = LogUtil().log()

