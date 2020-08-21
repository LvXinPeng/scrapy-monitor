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


        elif spider.name == "mysql":
            mysql_error_message = []

            # 1
            tm_vehicle_ability_cnt = item["tm_vehicle_ability_cnt"]
            if tm_vehicle_ability_cnt == 0:
                mysql_error_message.append("表tm_vehicle_ability 查询结果为 %d " % tm_vehicle_ability_cnt)

            # 2
            tm_vehicle_cnt = item["tm_vehicle_cnt"]
            if tm_vehicle_cnt == 0:
                mysql_error_message.append("表tm_vehicle 查询结果为 %d " % tm_vehicle_cnt)

            # 3
            tm_omd_vehicle_invoice_svw_cnt = item["tm_omd_vehicle_invoice_svw_cnt"]
            if tm_omd_vehicle_invoice_svw_cnt == 0:
                mysql_error_message.append("表tm_omd_vehicle_invoice_svw 查询结果为 %d" % tm_omd_vehicle_invoice_svw_cnt)

            # 4
            # tm_omd_vehicle_invoice_skd_cnt = item["tm_omd_vehicle_invoice_skd_cnt"]
            # if tm_omd_vehicle_invoice_skd_cnt == 0:
            #     mysql_error_message.append("表tm_omd_vehicle_invoice_skd 查询结果为 %d" % tm_omd_vehicle_invoice_skd_cnt)

            # 5
            tm_user_with_cp_cnt = item["tm_user_with_cp_cnt"]
            if tm_user_with_cp_cnt == 0:
                mysql_error_message.append("表tm_user_with_cp 查询结果为 %d" % tm_user_with_cp_cnt)

            # 6
            sel_tm_user_cnt = item["sel_tm_user_cnt"]
            if sel_tm_user_cnt == 0:
                mysql_error_message.append("表tm_users 查询结果为 %d" % sel_tm_user_cnt)

            # 7
            tr_party_account_role_cnt = item["tr_party_account_role_cnt"]
            if tr_party_account_role_cnt == 0:
                mysql_error_message.append("表tr_party_account_role 查询结果为 %d" % tr_party_account_role_cnt)

            # 调用邮箱发送
            if len(mysql_error_message) > 0:
                # 将列表mongodb_error_message转成字符串类型 error_message_str
                error_message_str = "<span style=\"background:#FFFF00;font-family:arial;color:black;font-size:18px;\">" + "<br>".join(mysql_error_message) + "</span>"

                mail_content = self.writer.write_content(spider.name, error_message_str)
                self.sender.send_email(settings.HOST, settings.SENDER_ACNT, settings.SENDER_PWD, mail_content,
                                       settings.MAIL_HEADER, settings.RECEIVERS)


        elif spider.name == "mongodb":
            mongodb_error_message = []

            # mongodbspider 的管道处理

            #  1. sel_area_history_cnt
            sel_area_history_cnt = item["sel_area_history_cnt"]
            if sel_area_history_cnt == 0 :
                # yesterday = '"%s"' % utils.yesterday.encode("utf-8")
                mongodb_error_message.append('_metric_activation_area_history 查询中执行结果不正常 ')

            # 2. sel_dealer_history_cnt
            sel_dealer_history_cnt = item["sel_dealer_history_cnt"]
            if sel_dealer_history_cnt == 0:
                # yesterday = '"%s"' % utils.yesterday.encode("utf-8")
                mongodb_error_message.append(
                    '_metric_activation_dealer_history 查询没有数据 。')

            # 3.1. sel_vehicle_cnt
            sel_vehicle_cnt = item["sel_vehicle_cnt"]
            if sel_vehicle_cnt == 0 or not sel_vehicle_cnt:
                mongodb_error_message.append('_metric_activation_area_now 查询 vehicle_cnt 字段没有数据')

            # 3.2. sel_activation_cnt
            sel_activation_cnt = item["sel_activation_cnt"]
            if sel_vehicle_cnt == 0 or not sel_activation_cnt:
                mongodb_error_message.append(
                    '_metric_activation_area_now 查询 activation_cnt 字段没有数据')

            # 4. sel_dealer_now_cnt
            sel_dealer_now_cnt = item["sel_dealer_now_cnt"]
            if sel_dealer_now_cnt == 0:
                mongodb_error_message.append('_metric_activation_dealer_now 的查询结果为0')

            # 5. sel_service_rank_cnt
            sel_service_rank_cnt = item["sel_service_rank_cnt"]

            intlastmonthmin = utils.intlastmonthmin

            service_rank_cnt = open("_metric_service_rank.txt", "a+")
            read = service_rank_cnt.read()  # 读数据

            if len(read) != 0 and sel_service_rank_cnt == int(read):
                # 昨天查询的和今天查询的数据相等，说明有异常
                mongodb_error_message.append(
                    "_metric_service_rank 的查询结果为: %d 与昨天查询的数据相等。(注: 如果结果为-1则说明没有查到数据) " % sel_service_rank_cnt)

            service_rank_cnt.truncate(0)  # 清空文件
            service_rank_cnt.write(str(sel_service_rank_cnt))  # 将今天数据存入
            service_rank_cnt.close()  # 关闭文件

            # 6. sel_oneapp_service_rank_cnt
            sel_oneapp_service_rank_cnt = item["sel_oneapp_service_rank_cnt"]

            # oneapp_metric_service_rank 是mongodb表名
            oneapp_service_rank_cnt = open("oneapp_metric_service_rank.txt", "a+")
            read = oneapp_service_rank_cnt.read()  # 读数据

            if len(read) != 0 and sel_oneapp_service_rank_cnt == int(read):
                # 昨天查询的和今天查询的数据相等，说明有异常
                mongodb_error_message.append(
                    "oneapp_metric_service_rank 的查询结果为: %d 与昨天查询的数据相等。(注: 如果结果为-1则说明没有查到数据) " % sel_oneapp_service_rank_cnt)

            oneapp_service_rank_cnt.truncate(0)  # 清空文件
            oneapp_service_rank_cnt.write(str(sel_oneapp_service_rank_cnt))  # 将今天数据存入
            oneapp_service_rank_cnt.close()  # 关闭文件

            # 7. sel_active_history_cnt
            sel_active_history_cnt = item["sel_active_history_cnt"]
            if sel_active_history_cnt == 0:
                mongodb_error_message.append("oneapp_metric_active_history 查询数据集为空")

            # 8. sel_active_now_cnt
            sel_active_now_cnt = item["sel_active_now_cnt"]
            if sel_active_now_cnt == 0:
                mongodb_error_message.append('oneapp_metric_active_now 查询数据集为空')

            # 9. sel_registry_history_cnt
            sel_registry_history_cnt = item["sel_registry_history_cnt"]

            if sel_registry_history_cnt == 0:
                mongodb_error_message.append('oneapp_metric_registry_history 查询数据集为空')

            # 10. sel_registry_now_cnt
            sel_registry_now_cnt = item["sel_registry_now_cnt"]
            if sel_registry_now_cnt == 0:
                mongodb_error_message.append('oneapp_metric_registry_now 查询结果集为空 ')

            # 11. sel_type_now_cnt
            sel_type_now_cnt = item["sel_type_now_cnt"]
            if sel_type_now_cnt == 0:
                mongodb_error_message.append('oneapp_metric_user_type_now 查询结果集为空 ')

            # 调用邮箱发送
            if len(mongodb_error_message) > 0:
                # 将列表mongodb_error_message转成字符串类型 error_message_str
                error_message_str = "<span style=\"background:#FFFF00;font-family:arial;color:black;font-size:18px;\">" + "<br>".join(mongodb_error_message) + "</span>"
                mail_content = self.writer.write_content(spider.name, error_message_str)
                self.sender.send_email(settings.HOST, settings.SENDER_ACNT, settings.SENDER_PWD, mail_content,
                                       settings.MAIL_HEADER, settings.RECEIVERS)


        return item
