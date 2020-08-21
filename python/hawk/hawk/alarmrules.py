# -*- coding:utf-8 -*-
class AlarmRules(object):
    """
    该类用来处理pipeline获得的数据
    """

    def write_content(self, component, content):
        """
        该方法处理pipeline获得的数据，并生成异常邮件的正文内容
        :param component: 被监控组件对应的爬虫名称
        :param content: 异常值
        :return: 邮件正文内容
        """
        component_name = str(component).replace("Spider", "")
        exception_content = ["""
        <p style="font-family:verdana;font-size:17px;">Hi All,</p>
        <p style="font-family:arial;color:black;font-size:17px;">[<b><em>%s</em></b>]出现异常，异常详细：</p>
        <span style="background:#FFFF00;font-family:arial;color:black;font-size:19px;"><b>%s</b></span>
        <p style="font-family:arial;color:black;font-size:17px;">请尽快排查问题并修复。</p>
        <p style="font-family:arial;color:black;font-size:17px;">Best Regards,</p>
        <p style="font-family:arial;color:black;font-size:17px;">XXX</p>
        """ % (component_name, str(content))]
        return exception_content[0]