#!/usr/bin/env python3
import os

#公共变量
#setting.py文件的绝对路径
abs_path = os.path.abspath(__file__)

#项目存放路径
project_path = os.path.dirname(os.path.dirname(abs_path))

#日志文件存放路径
log_path = project_path + os.sep + 'log'

#报告数据存放路径
report_path = project_path + os.sep + 'report'


#数据文件存放路径
data_path = project_path + os.sep + 'data'


# usages
class CommonVar:
    def __init__(self):
        self.cookie = None   #存放测试过程中获取到的Cookie信息
        self.cart_id_list = []   #存放商品的cart_id
        self.order_id = None   #存放订单id
        self.order_detail_id = None   #存放订单详情id



