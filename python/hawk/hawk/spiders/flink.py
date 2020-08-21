# -*- coding: utf-8 -*-
import json
import logging
import hawk.items
import scrapy
import os
from scrapy import Request
if os.environ.get('SCRAPY_PROJECT') == 'uat':
    from hawk import uat_settings as settings
elif os.environ.get('SCRAPY_PROJECT') == 'prod':
    from hawk import prod_settings as settings


class FlinkSpider(scrapy.Spider):
    name = 'flink'
    allowed_domains = [settings.FLINK_HOST_IP]
    start_url = 'http://{host}:{port}/proxy/{application_id}/jobs/overview'
    # init application_id list
    app_list = []
    # init application_id dict
    app_dict = {}
    global app_dict

    for job in settings.FLINK_JOB_NAME:
        yarn_cmd = 'yarn application -list | grep "%s" | cut -f 1' % job
        # get application_id
        app_result = os.popen(yarn_cmd).readlines()[0]
        # format application_id
        app_id = app_result.replace('\n', '')
        # get application_id list
        app_list.append(app_id)
        # get application_id dict
        app_dict[app_id] = job

    def start_requests(self):
        logging.info("begin parse")
        for application_id in self.app_list:
            # get current application id
            global tmp_application_id
            tmp_application_id = application_id
            yield Request(self.start_url.format(host=settings.FLINK_HOST_IP, port=settings.FLINK_HOST_PORT,
                                                application_id=application_id), callback=self.parse, method='GET',
                          meta={'cookiejar': 1}, headers={"Content-Type": "application/json"})

    def parse(self, response):
        flink_item = hawk.items.FlinkItem()
        print("====parse flink state====")
        logging.info("===%s==%s===",app_dict[tmp_application_id],tmp_application_id)
        flink_item['job_name'] = app_dict[tmp_application_id]
        flink_item['job_id'] = tmp_application_id

        logging.debug("flink job result:%s", response.text)
        flink_job_json = json.loads(response.text)
        # Flink job Crashed ==> Flink WebUI shows failed 1 & Yarn WebUI shows RUNNING;
        # But response json is null ==> {"jobs":[]}
        if len(flink_job_json["jobs"]) == 0:
            flink_item['job_finished_cnt'] = 0
            flink_item['job_canceled_cnt'] = 0
            flink_item['job_failed_cnt'] = 1
        else:
            job_finished_cnt = flink_job_json["jobs"][0]["tasks"]["finished"]
            job_canceled_cnt = flink_job_json["jobs"][0]["tasks"]["canceled"]
            job_failed_cnt = flink_job_json["jobs"][0]["tasks"]["failed"]
            logging.info("crawl job finished count: %d", job_finished_cnt)
            logging.info("crawl job canceled count: %d", job_canceled_cnt)
            logging.info("crawl job failed count: %d", job_failed_cnt)

            flink_item['job_finished_cnt'] = job_finished_cnt
            flink_item['job_canceled_cnt'] = job_canceled_cnt
            flink_item['job_failed_cnt'] = job_failed_cnt

        yield flink_item
