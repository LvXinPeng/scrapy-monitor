# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from hawk import utils
from hawk.items import mongodbItem
import logging
import os
if os.environ.get('SCRAPY_PROJECT') == 'uat':
    from hawk import uat_settings as settings
elif os.environ.get('SCRAPY_PROJECT') == 'prod':
    from hawk import prod_settings as settings


"""
    监控mongodb是否运行正常。
"""

class MongodbSpider(scrapy.Spider):
    name = 'mongodb'
    #！无效url，只是为了满足框架需要
    allowed_domains = ['']
    start_urls = ['']

    # 创建连接
    def connect_mongo(self):
        # 创建mongodb 连接
        mongo_jdbc = settings.MOGODB_JDBC
        mongo_client = MongoClient(mongo_jdbc)

        return mongo_client

    # 1. _metric_activation_area_history 当月只有一条，且数据更新时间update_time为当前时间的前一天
    def query_from_area_history(self, _dashboard_db):

        mogo_col = _dashboard_db["_metric_activation_area_history"]

        yesterday= utils.yesterday
        sel_area_history_cnt = mogo_col.find({"hu_type": "all", "vehicle_model": "all", "province": "all", "area": "all",
                                   "update_time": yesterday}).count()


        return sel_area_history_cnt

    # 2. _metric_activation_dealer_history update_time为前一天查询数据是否存在，有则为正常
    def query_from_dealer_history(self, _dashboard_db):

        mogo_col = _dashboard_db["_metric_activation_dealer_history"]

        yesterday = utils.yesterday

        sel_dealer_history_cnt= mogo_col.find({"hu_type": "all", "vehicle_model": "all", "province": "all", "area": "all",
                                     "update_time": yesterday}).count()


        return sel_dealer_history_cnt

    # 3. _metric_activation_area_now  获取结果集中的activation_cnt，vehicle_cnt 查看该表是否有数据，有则为正常
    def query_from_area_now(self, _dashboard_db):

        mogo_col = _dashboard_db["_metric_activation_area_now"]

        sel_area_now_array = mogo_col.find({'province': 'all', 'area': 'all', 'hu_type': 'all', 'vehicle_model': 'all'},
                              {"_id": 0, "activation_cnt": 1, "vehicle_cnt": 1})


        for i in sel_area_now_array:
            # self.item["vehicle_cnt"] = i["vehicle_cnt"]
            # self.item["activation_cnt"] = i["activation_cnt"]
            return i["vehicle_cnt"],i["activation_cnt"]

    # 4. _metric_activation_dealer_now  查看该表是否有数据，有则为正常
    def query_from_dealer_now(self, _dashboard_db):

        mogo_col = _dashboard_db["_metric_activation_dealer_now"]

        sel_dealer_now_cnt = mogo_col.find({'province': 'all', 'area': 'all', 'hu_type': 'all', 'vehicle_model': 'all'}).count()

        return sel_dealer_now_cnt


    # 5 _metric_service_rank  查看user_cnt字段是否有更新 （通过记录文件的方式）
    def query_from_service_rank(self, _dashboard_db):
        mogo_col = _dashboard_db["_metric_service_rank"]
        intcurrentmonth = utils.intcurrentmonthmin

        sel_user_cnt = mogo_col.find(
            {'area': 'all', 'hu_type': 'all', 'month': intcurrentmonth, 'vehicle_model': 'all', 'province': 'all'},
            {"_id": 0, "user_cnt": 1})

        count = sel_user_cnt.count()

        con = -1

        if count != 0:
            for i in sel_user_cnt:
                if i["user_cnt"]:

                    con = i["user_cnt"]

        return con

    # 6 oneapp_metric_service_rank  查看user_cnt字段是否有更新 （通过记录文件的方式）
    def query_from_oneapp_service_rank(self, _dashboard_db):
        intcurrentmonthmin = utils.intcurrentmonthmin
        mogo_col = _dashboard_db["oneapp_metric_service_rank"]
        sel_oneapp_user_cnt = mogo_col.find(
            {'area': 'all', 'user_type': 'all', 'month': intcurrentmonthmin, 'province': 'all'},
            {"_id": 0, "user_cnt": 1})

        count = sel_oneapp_user_cnt.count()
        con = -1
        if count != 0:
            for i in sel_oneapp_user_cnt:
                if i["user_cnt"]:
                    con = i["user_cnt"]

        return con

    # 7 oneapp_metric_active_history  month当前月份前一个月，例：当前是2020年6月份，那month为202005，结果集不为空即正常
    def query_from_active_history(self, _dashboard_db):
        mogo_col = _dashboard_db["oneapp_metric_active_history"]
        intlastmonth = utils.intlastmonth
        sel_active_history_cnt = mogo_col.find(
            {'area': 'all', 'user_type': 'all', 'month': intlastmonth, 'province': 'all'}).count()

        return sel_active_history_cnt

    # 8 oneapp_metric_active_now  有数据即正常
    def query_from_active_now(self, _dashboard_db):
        mogo_col = _dashboard_db["oneapp_metric_active_now"]

        sel_active_now_cnt = mogo_col.find({'area': 'all'}).count()

        return sel_active_now_cnt

    # 9 oneapp_metric_registry_history   month为当前月份，有数据即正常
    def query_from_registry_history(self, _dashboard_db):
        mogo_col = _dashboard_db["oneapp_metric_registry_history"]
        intcurrentmonth = utils.intcurrentmonth
        sel_registry_history_cnt = mogo_col.find({'area': 'all', 'month': intcurrentmonth}).count()

        return sel_registry_history_cnt

    # 10 oneapp_metric_registry_now   有数据即正常
    def query_from_registry_now(self, _dashboard_db):
        mogo_col = _dashboard_db["oneapp_metric_registry_now"]

        sel_registry_now_cnt = mogo_col.find({'area': 'all'}).count()

        return sel_registry_now_cnt

    # 11 oneapp_metric_user_type_now  有数据即正常
    def query_from_type_now(self, _dashboard_db):
        mogo_col = _dashboard_db["oneapp_metric_user_type_now"]

        sel_type_now_cnt = mogo_col.find().count()

        return sel_type_now_cnt

    def parse(self, response):
        logging.info("begin to parse mongodbspider.")
        item = mongodbItem()
        try:

            mongo_client = self.connect_mongo()
            # 连接到 _dashboard 数据库
            _dashboard_db = mongo_client["_dashboard"]

            # 1. _metric_activation_area_history
            sel_area_history_cnt = self.query_from_area_history(_dashboard_db)
            item["sel_area_history_cnt"] = sel_area_history_cnt


            # 2. _metric_activation_dealer_history
            sel_dealer_history_cnt = self.query_from_dealer_history(_dashboard_db)
            item["sel_dealer_history_cnt"] = sel_dealer_history_cnt


            # 3. _metric_activation_area_now
            vehicle_activation_cnts = self.query_from_area_now(_dashboard_db)
            item["sel_vehicle_cnt"] = vehicle_activation_cnts[0]
            item["sel_activation_cnt"] = vehicle_activation_cnts[1]

            # 4. _metric_activation_dealer_now
            sel_dealer_now_cnt = self.query_from_dealer_now(_dashboard_db)
            item["sel_dealer_now_cnt"] = sel_dealer_now_cnt

            # 5 _metric_service_rank
            service_rank = self.query_from_service_rank(_dashboard_db)
            item["sel_service_rank_cnt"] = service_rank

            # 6 oneapp_metric_service_rank
            oneapp_service_rank = self.query_from_oneapp_service_rank(_dashboard_db)
            item["sel_oneapp_service_rank_cnt"] = oneapp_service_rank

            # 7 oneapp_metric_active_history
            sel_active_history_cnt = self.query_from_active_history(_dashboard_db)
            item["sel_active_history_cnt"] = sel_active_history_cnt

            # 8 oneapp_metric_active_now
            sel_active_now_cnt = self.query_from_active_now(_dashboard_db)
            item["sel_active_now_cnt"] = sel_active_now_cnt

            # 9 oneapp_metric_registry_history
            sel_registry_history_cnt = self.query_from_registry_history(_dashboard_db)
            item["sel_registry_history_cnt"] = sel_registry_history_cnt

            # 10 oneapp_metric_registry_now
            sel_registry_now_cnt = self.query_from_registry_now(_dashboard_db)
            item["sel_registry_now_cnt"] = sel_registry_now_cnt

            # 11 oneapp_metric_user_type_now
            sel_type_now_cnt = self.query_from_type_now(_dashboard_db)
            item["sel_type_now_cnt"] = sel_type_now_cnt

            logging.info("end of parse mongodbspider")

            yield item

        except Exception as e:
            logging.error("连接失败", e)
            return

        finally:
            # 关闭连接
            mongo_client.close()
