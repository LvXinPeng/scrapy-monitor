# -*- coding:utf-8 -*-
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP
import logging


class MailSender(object):
    """
    该类用来管理发送邮件的对象
    """

    def send_email(self, host, sender_acnt, sender_pwd, mail_content, mail_title, receiver):
        """
        该方法用来发送异常警告邮件
        :param self:
        :param host: SMTP服务器地址
        :param sender_acnt: 发件人邮箱账号
        :param sender_pwd: 发件人邮箱密码
        :param mail_content: 邮件正文
        :param mail_title: 邮件标题
        :param receiver: 收件人邮箱账号
        """
        # 登录
        smtp = SMTP(host)
        smtp.set_debuglevel(0)
        smtp.starttls()
        smtp.ehlo(host)
        smtp.login(sender_acnt, sender_pwd)
        # 邮件内容
        msg = MIMEText(mail_content, "html", "utf-8")
        msg["Subject"] = Header(mail_title, "utf-8")
        msg["From"] = sender_acnt
        msg["To"] = ','.join(receiver)
        send_mail_info = smtp.sendmail(sender_acnt, receiver, msg.as_string())
        logging.info("%s" % (send_mail_info))
        smtp.quit()
