# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class HawkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SensorItem(scrapy.Item):
    received_events_num = Field()
    validated_events_num = Field()
    saved_events_num = Field()
    error_events_num = Field()
    pass


class AirflowItem(scrapy.Item):
    dag_state = scrapy.Field()
    pass


class FlinkItem(scrapy.Item):
    job_name = scrapy.Field()
    job_id = scrapy.Field()
    job_finished_cnt = scrapy.Field()
    job_canceled_cnt = scrapy.Field()
    job_failed_cnt = scrapy.Field()
    pass


class MysqlItem(scrapy.Item):
    # 数据库名称：mos-gvs-mysql-vehicle
    tm_vehicle_ability_cnt = scrapy.Field()
    tm_vehicle_cnt = scrapy.Field()

    # 数据库名称： mos-lsif-mysql-main
    tm_omd_vehicle_invoice_svw_cnt = scrapy.Field()
    tm_omd_vehicle_invoice_skd_cnt = scrapy.Field()

    # 数据库名称：mos-tcrm-mysql-main
    tm_user_with_cp_cnt = scrapy.Field()
    sel_tm_user_cnt = scrapy.Field()
    tr_party_account_role_cnt = scrapy.Field()

    # SqlList = settings.LIST
    #
    # for sql in SqlList:
    #     TableName = sql.split('@')[1]
    #     TableName = scrapy.Field()


class mongodbItem(scrapy.Item):
    sel_area_history_cnt = scrapy.Field()

    sel_dealer_history_cnt = scrapy.Field()
    sel_vehicle_cnt = scrapy.Field()
    sel_activation_cnt = scrapy.Field()

    sel_dealer_now_cnt = scrapy.Field()
    sel_service_rank_cnt = scrapy.Field()
    sel_oneapp_service_rank_cnt = scrapy.Field()

    sel_active_history_cnt = scrapy.Field()
    sel_active_now_cnt = scrapy.Field()
    sel_registry_history_cnt = scrapy.Field()

    sel_registry_now_cnt = scrapy.Field()
    sel_type_now_cnt = scrapy.Field()


class DiskItem(scrapy.Item):
    proportion = scrapy.Field()


