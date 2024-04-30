#!/usr/bin/env python3
import os.path
import time
import datetime

import allure
#import pytest
import requests
import requests.utils
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


class Test_Cart_Show_Products:
    def setup_class(self):
        logger.info(f"******************keystone官网商城下单测试执行开始,开始时间{current_time}***********************")


    # @allure.title("购物车添加商品")
    # @pytest.mark.parametrize("goods",read_data("../data/goods.txt"))
    cart_id = "gid://shopify/Cart/Z2NwLWV1cm9wZS13ZXN0MTowMUhXOVlNQTdQNk1INUhNV1JCMlRCNVE2WQ"
    product_id = "gid://shopify/ProductVariant/43296530301081"   #Keystone 3Pro
    quantity = 2
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

    
    id = "gid://shopify/CartLine/9af19807-60d9-461e-945c-ef9c6c6ebd52?cart=Z2NwLWV1cm9wZS13ZXN0MTowMUhXOVlNQTdQNk1INUhNV1JCMlRCNVE2WQ"
    goods1 = {
    "id":id,
    "products": [{"product":product_id},{"quantity":1}]}
    def test_cart_update_goods(self,goods1):
        url = "https://api-staging.keyst.one/v1/web/add_products_to_cart/"
        method = "post"
        logger.info("更新购物车商品测试用例")
        with allure.step("发送请求"):
            res = requests.post(url=url, method=method, data=goods1)
        with allure.step("判断返回数据"):
            logger.info("返回数据为：{}".format(res.json()))
            assert res.json().get('status') == 200


    #查询购物车
    @allure.title("查询购物车")
    def test_cart_check(self):
        url = "https://api.keyst.one/v1/web/shop_cart/"
        id = "gid://shopify/Cart/c1-2e953ed3f74c0a2125b6d67722bdf8c2"
        method = "get"
        logger.info("查询购物车列表")
        with allure.step("发送请求"):
            res = requests.get(url,data={id: "id"})
        with allure.step("获取商品的cart_id号"):
            if res.status_code == 200:
                # 解析响应数据，获取购物车中的所有商品
                cart_items = res.json()
                # 遍历商品列表，全选商品
                cart_count = []
                for item in cart_items:
                    cart_items.append(item["id"])
                if len(cart_items) == 2:
                    logger.info("购物车商品数量正确")
                    assert True
                else:
                    logger.info("购物车商品数量有问题")
                    assert False   
                    
                                 
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
