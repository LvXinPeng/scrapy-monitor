# -*- coding: utf-8 -*-
import scrapy
import pymysql
import logging
from hawk.items import MysqlItem
from hawk import utils
import os
if os.environ.get('SCRAPY_PROJECT') == 'uat':
    from hawk import uat_settings as settings
elif os.environ.get('SCRAPY_PROJECT') == 'prod':
    from hawk import prod_settings as settings


"""
    监控MySQL数据库中 是否存在update_time大于今天的数据 如果不存在则为异常数据

    -gvs-mysql-vehicle库: tm_vehicle、tm_vehicle_ability 

    -lsif-mysql-main库： tm_omd_vehicle_invoice_、tm_omd_vehicle_invoice_ 

    -tcrm-mysql-main库： tm_user_with_cp、tm_users、tr_party_account_role
"""


class MysqlSpider(scrapy.Spider):
    name = 'mysql'
    # ！无效url，只是为了满足框架需要
    allowed_domains = ['']
    start_urls = ['']

    # 获取当前日期  ： 2020-06-29
    # curr_date = datetime.datetime.now().date()
    yesterday = utils.yesterday
    yester_day = "'%s'" % yesterday

    item = MysqlItem()
    host = settings.MYSQL_HOST
    user = settings.MYSQL_USER
    password = settings.MYSQL_PASSWORD

    def parse(self, response):
        logging.info("begin to parse mysqlspider.")

        try:

            # 创建 -gvs-mysql-vehicle库 连接
            conn_vehicle = self.get_connect("-gvs-mysql-vehicle")
            # 创建 -lsif-mysql-main 库 连接
            conn_lsif = self.get_connect("-lsif-mysql-main")
            # 创建 -tcrm-mysql-main 库 连接
            conn_tcrm = self.get_connect("-tcrm-mysql-main")
            # 监控 -gvs-mysql-vehicle 库下面的两张表监控 tm_vehicle_ability，tm_vehicle
            self.moniter_tm_vehicle_ability_cnt(conn_vehicle)
            self.moniter_tm_vehicle_cnt(conn_vehicle)

            # 监控 -lsif-mysql-main 库下面的两张表监控 tm_omd_vehicle_invoice_，tm_omd_vehicle_invoice_
            self.moniter_tm_omd_vehicle_invoice__cnt(conn_lsif)
            #self.moniter_tm_omd_vehicle_invoice__cnt(conn_lsif)

            # 监控 -tcrm-mysql-main 库下面的三张表监控 tm_user_with_cp，tm_users，tr_party_acresult_role
            self.moniter_tm_user_with_cp_cnt(conn_tcrm)
            self.moniter_tm_user_cnt(conn_tcrm)
            self.moniter_tr_party_account_role_cnt(conn_tcrm)

        except Exception as e:
            print("失败", e)
            logging.info("连接失败", e)
            return

        finally:
            # 关闭连接
            conn_vehicle.close()
            conn_lsif.close()
            conn_tcrm.close()

        logging.info("end of parse mysqlspider")

        yield self.item

    # pymysql 创建 -gvs-mysql-vehicle 连接
    def get_connect(self, database):
        # 创建数据库连接
        conn = pymysql.connect(self.host, self.user, self.password,
                               database,
                               port=6033)
        return conn

    # 查询tm_vehicle_ability表 sql
    def moniter_tm_vehicle_ability_cnt(self, conn_vehicle):
        sql = "select count(1) from tm_vehicle_ability  where DATE_FORMAT(update_time,'%Y-%m-%d')>=  " + self.yester_day;

        # 创建游标对象
        cursor_vehicle = conn_vehicle.cursor()

        # 执行sql
        cursor_vehicle.execute(sql)
        # 处理结果
        result = cursor_vehicle.fetchone()

        self.item["tm_vehicle_ability_cnt"] = result[0]

    # 查询tm_vehicle表 sql
    def moniter_tm_vehicle_cnt(self, conn_vehicle):
        sql = """
                                select count(1) from tm_vehicle  where DATE_FORMAT(update_time,'%Y-%m-%d')>= 
                                """
        sql = sql + self.yester_day
        # 创建游标对象
        cursor = conn_vehicle.cursor()
        # 执行sql
        cursor.execute(sql)
        # 处理结果
        result = cursor.fetchone()
        self.item["tm_vehicle_cnt"] = result[0]

    # ------------------------------------------------------------------------------------------------------------------

    def moniter_tm_omd_vehicle_invoice__cnt(self, conn_lsif):
        sql = """
                                select count(1) from tm_omd_vehicle_invoice_  where DATE_FORMAT(update_time,'%Y-%m-%d')>= 
                                """
        sql = sql + self.yester_day

        # 创建游标对象
        cursor = conn_lsif.cursor()

        # 执行sql
        cursor.execute(sql)

        # 处理结果
        result = cursor.fetchone()

        self.item["tm_omd_vehicle_invoice__cnt"] = result[0]

    def moniter_tm_omd_vehicle_invoice__cnt(self, conn_lsif):
        sql = """
                                select count(1) from tm_omd_vehicle_invoice_  where DATE_FORMAT(update_time,'%Y-%m-%d')>= 
                                """
        sql = sql + self.yester_day

        # 创建游标对象
        cursor = conn_lsif.cursor()

        # 执行sql
        cursor.execute(sql)
        # 处理结果
        result = cursor.fetchone()
        self.item["tm_omd_vehicle_invoice__cnt"] = result[0]

    # ------------------------------------------------------------------------------------------------------------------

    def moniter_tm_user_with_cp_cnt(self, conn_tcrm):
        sql = """
                                select count(1) from tm_user_with_cp  where DATE_FORMAT(update_time,'%Y-%m-%d')>= 
                                """
        sql = sql + self.yester_day

        # 创建游标对象
        cursor = conn_tcrm.cursor()

        # 执行sql
        cursor.execute(sql)

        # 处理结果
        result = cursor.fetchone()

        self.item["tm_user_with_cp_cnt"] = result[0]

    def moniter_tm_user_cnt(self, conn_tcrm):
        sql = "select count(1) from tm_users  where DATE_FORMAT(update_time,'%Y-%m-%d')>= "

        sql = sql + self.yester_day

        # 创建游标对象
        cursor = conn_tcrm.cursor()

        # 执行sql
        cursor.execute(sql)

        # 处理结果
        result = cursor.fetchone()

        self.item["sel_tm_user_cnt"] = result[0]

    def moniter_tr_party_account_role_cnt(self, conn_tcrm):
        sql = """
                                select count(1) from tr_party_account_role  where DATE_FORMAT(update_time,'%Y-%m-%d')>= 
                                """
        sql = sql + self.yester_day

        # 创建游标对象
        cursor = conn_tcrm.cursor()

        # 执行sql
        cursor.execute(sql)

        # 处理结果
        result = cursor.fetchone()

        self.item["tr_party_account_role_cnt"] = result[0]
