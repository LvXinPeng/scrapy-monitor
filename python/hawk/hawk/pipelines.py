# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from hawk import mailsender
from hawk import alarmrules
from hawk import utils
import os
if os.environ.get('SCRAPY_PROJECT') == 'uat':
    from hawk import uat_settings as settings
elif os.environ.get('SCRAPY_PROJECT') == 'prod':
    from hawk import prod_settings as settings


class HawkPipeline(object):

    def open_spider(self, spider):
        """
        声明MailSender和AlarmRules对象
        """
        self.sender = mailsender.MailSender()
        self.writer = alarmrules.AlarmRules()

    def process_item(self, item, spider):
        if spider.name == "sensor":
            # 将获取的值与异常临界值做判断
            if item["received_events_num"] == 0:
                item_content = "The number of events received by Sensor is 0."
                mail_content = self.writer.write_content(spider.name, item_content)
                self.sender.send_email(settings.HOST, settings.SENDER_ACNT, settings.SENDER_PWD, mail_content,
                                       settings.MAIL_HEADER, settings.RECEIVERS)
                return item
        elif spider.name == "airflow":
            if item["dag_state"] != 'success':
                dag_state = "Airflow job %s crashed ==> http://%s" % (settings.AIRFLOW_DAG_NAME, settings.AIRFLOW_HOST)
                mail_content = self.writer.write_content(spider.name, dag_state)
                self.sender.send_email(settings.HOST, settings.SENDER_ACNT, settings.SENDER_PWD, mail_content,
                                       settings.MAIL_HEADER, settings.RECEIVERS)
                return item
        elif spider.name == "flink":
            if item["job_failed_cnt"] > 0:
                flink_state = "Flink job %s crashed ==> %s%s" % (item["job_name"], settings.YARN_HOST, item["job_id"])
                mail_content = self.writer.write_content(spider.name, flink_state)
                self.sender.send_email(settings.HOST, settings.SENDER_ACNT, settings.SENDER_PWD, mail_content,
                                       settings.MAIL_HEADER, settings.RECEIVERS)

        elif spider.name == "disk":
            disk_proportion = item["proportion"]

            result_proportion = disk_proportion.split("%")[0]

            if (int(result_proportion) > 80):
                disk_anomaly = "Disk utilization reached %s " % disk_proportion
                mail_content = self.writer.write_content(spider.name, disk_anomaly)
                self.sender.send_email(settings.HOST, settings.SENDER_ACNT, settings.SENDER_PWD, mail_content,
                                       settings.MAIL_HEADER, settings.RECEIVERS)


        


        return item
