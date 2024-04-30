#!/usr/bin/env python3
import json
import re
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urllib import parse


#读取json格式文件内容
def read_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)
    

#读取txt文档内容并返回文档内容
def read_txt_file(filepath):
    with open(filepath, 'r') as f:
        line = []  #因商品有两条数据，所以使用列表保存
        for data in f:
            if data[-1] == "\n":
                data = data[:-1]
            line.append(data)
        return line


#将字符串格式转换为字典格式
def str_to_dict(content):
    words = parse.unquote(content, encoding='utf-8') + "&"   #字符串转换为utf8编码的字符串
    pattern = "(.*?)=(.*?)&"    #通配符
    list_tmp = re.findall(pattern,words)   #找出数据中的所有键值对，以元组形式存放在临时列表中
    # 将列表数据转为字典
    dict_tmp = {}
    for i in range(len(list_tmp)):
        dict_tmp[list_tmp[i][0]] = list_tmp[i][i]
    return dict_tmp


#读取txt文档，转换为json格式的数据，存放到列表中，并返回
def read_data(filepath):
    data_list = read_txt_file(filepath)  #从txt文档中读取数据
    data_dict_list = []
    for data in data_list:   #将数据转换为字典类型后存入
        data_dict_list.append(str_to_dict(data))
    return data_dict_list
