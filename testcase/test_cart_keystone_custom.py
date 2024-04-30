#!/usr/bin/env python3
import os.path
import time
import datetime

import allure
#import pytest
import requests
import requests.utils
# 把当前文件所在文件夹的父文件夹路径加入到PYTHONPATH
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from api.api_run import ApiRun
#from common.settings import CommonVar, data_path
from tools.logUtils import logger
#from tools.readData import read_json, read_data


#初始化类
#api_run = ApiRun()
#common = CommonVar()
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Test_Cart_Keystone_Accessories_And_Partnership:
    def setup_class(self):
        logger.info(f"******************keystone官网商城下单测试执行开始,开始时间{current_time}***********************")


    # @allure.title("购物车添加商品")
    # @pytest.mark.parametrize("goods",read_data("../data/goods.txt"))
    cart_id = "gid://shopify/Cart/c1-104b00ba8d5741d4ca33414587cffc6b"
    product_id = "gid://shopify/ProductVariant/43545798377625"   #Keystone Custom Version
    quantity = 1
    goods = { 
    "cart_id":cart_id,
    "products": [{"product":product_id},{"quantity":quantity}]}
    def test_cart_add_goods(self,goods):
        url = "https://api-staging.keyst.one/v1/web/add_products_to_cart/"
        method = "post"
        logger.info("往购物车添加商品测试用例")
        with allure.step("发送请求"):
            res = requests.post(url=url, method=method, data=goods)
        with allure.step("判断返回数据"):
            logger.info("返回数据为：{}".format(res.json()))
            assert res.json().get('status') == 200

    #购物车下单
    @allure.title("购物车下单")
    def test_cart_checkout(self):
        url = "https://tracking.refersion.com/checkout"
        checkout_id = "Z2NwLWV1cm9wZS13ZXN0MTowMUhXOVlNQTdQNk1INUhNV1JCMlRCNVE2WQ"
        id = "e0defc6c2cfa564c996319ae6006c583"
        method = "post"
        logger.info("从购物车下单")
        with allure.step("发送请求"):
            res = requests.post(url=url, method=method, checkout_id=checkout_id, id=id)
        with allure.step("判断返回数据"):
            logger.info("返回数据为：{}".format(res.json()))
            assert res.json().get('status') == 200                


    def teardown_class(self):
        logger.info(f"******************keystone官网商城下单测试执行结束,结束时间{current_time}***********************")
