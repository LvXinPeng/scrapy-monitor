# -*- coding: utf-8 -*-
import scrapy
import os
from hawk.items import DiskItem

class DiskSpider(scrapy.Spider):

    name = 'disk'
    # ！无效url，只是为了满足框架需要
    allowed_domains = ['']
    start_urls = []

    def parse(self, response):
        item = DiskItem()

        select_disk = " df -h /|awk 'NR==2{print $5}' "

        disk_result = os.popen(select_disk).readlines()[0]

        disk_proportion = disk_result.replace('\n', '')

        item["proportion"] = disk_proportion

        yield item
