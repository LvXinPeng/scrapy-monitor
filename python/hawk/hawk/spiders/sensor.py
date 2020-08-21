# -*- coding: utf-8 -*-
import scrapy
import logging
import json
from scrapy import FormRequest, Request, http
import time, datetime
import hawk.items
import os
if os.environ.get('SCRAPY_PROJECT') == 'uat':
    from hawk import uat_settings as settings
elif os.environ.get('SCRAPY_PROJECT') == 'prod':
    from hawk import prod_settings as settings


class SensorSpider(scrapy.Spider):
    name = 'sensor'
    allowed_domains = [settings.SENSOR_HOST_IP]
    start_urls = ['http://{host}:{port}/api/auth/login?project=App']
    report_url = 'http://{host}:{port}/api/data_source/report'
    custom_settings = {}

    def start_requests(self):
        logging.info("begin parse")
        data = {
            'username': settings.SENSOR_USERNAME,
            'password': settings.SENSOR_PWD,
            'expired_interval': 10080
        }
        for url in self.start_urls:
            yield Request(url.format(host=settings.SENSOR_HOST_IP, port=settings.SENSOR_HOST_PORT),
                          callback=self.parse_login, method='POST', meta={'cookiejar': 1},
                          headers={"Content-Type": "application/json"}, body=json.dumps(data),
                          errback=self.error_handle)

    def parse_login(self, response):
        resultdata = json.loads(response.text)
        logging.info("result data:%s", resultdata)
        fromL, toL = self.in_one_hour()
        report_data = {
            "lib": "Logstash",
            "from": fromL,
            "to": toL,
            "app_version": "all",
            "status": "all"
        }
        logging.debug("crawl data from : %s, to : %s", str(datetime.datetime.fromtimestamp(fromL / 1000)),
                      str(datetime.datetime.fromtimestamp(toL / 1000)))
        yield Request(self.report_url.format(host=settings.SENSOR_HOST_IP, port=settings.settings.SENSOR_HOST_PORT),
                      callback=self.parse_report, method='POST', meta={'cookiejar': response.meta['cookiejar']},
                      headers={'Sensorsdata-Project': 'App', "Content-Type": "application/json",
                               'Accept-Encoding': None, 'User-Agent': None}, body=json.dumps(report_data),
                      errback=self.error_handle)

    def parse_report(self, response):
        print("====parse report====")
        logging.debug("report result:%s", response.text)
        report_data_json = json.loads(response.text)
        read_hu_msg_count = report_data_json.get("detail").get("read")
        logging.info("crawl hu msg count: %s", read_hu_msg_count)

        sensor_item = hawk.items.SensorItem()
        sensor_item['received_events_num'] = report_data_json.get("detail").get("read")
        sensor_item['validated_events_num'] = report_data_json.get("detail").get("send")
        sensor_item['error_events_num'] = report_data_json.get("detail").get("err")

        yield sensor_item

    def error_handle(self, response):
        logging.debug("=======report header========:%s", response.request.headers)
        print("error handle.")
        logging.error(response)

    def in_one_hour(self):
        now = time.time() * 1000
        one_hour_ago = now - 3600 * 1000L
        return one_hour_ago, now
