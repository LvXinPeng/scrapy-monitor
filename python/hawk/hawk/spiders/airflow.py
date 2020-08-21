# -*- coding: utf-8 -*-
import json
import logging
import hawk.items
import arrow
import scrapy
from scrapy import Request
import os
if os.environ.get('SCRAPY_PROJECT') == 'uat':
    from hawk import uat_settings as settings
elif os.environ.get('SCRAPY_PROJECT') == 'prod':
    from hawk import prod_settings as settings


class AirflowSpider(scrapy.Spider):
    name = 'airflow'
    allowed_domains = [settings.AIRFLOW_HOST]
    start_url = 'http://{host}/api/experimental/dags/{dags}/dag_runs/{date}T{time}+00:00'
    dags = settings.AIRFLOW_DAG_NAME
    date_now = arrow.now().shift(days=-2).format("YYYY-MM-DD")
    time_now = settings.AIRFLOW_DAG_SCHEDULE_TIME

    def start_requests(self):
        logging.info("begin parse")

        yield Request(
            self.start_url.format(host=settings.AIRFLOW_HOST, dags=self.dags,
                                  date=self.date_now, time=self.time_now), callback=self.parse, method='GET',
            meta={'cookiejar': 1}, headers={"Content-Type": "application/json"})

    def parse(self, response):
        print("====parse dag state====")
        logging.debug("report result:%s", response.text)
        state_data_json = json.loads(response.text)
        dag_state = state_data_json.get("state")
        logging.info("crawl state: %s", dag_state)

        airflow_item = hawk.items.AirflowItem()
        airflow_item['dag_state'] = state_data_json.get("state")

        yield airflow_item
