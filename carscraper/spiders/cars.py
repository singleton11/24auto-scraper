# -*- coding: utf-8 -*-
import scrapy


class CarsSpider(scrapy.Spider):
    name = "cars"
    start_urls = ['http://24auto.ru/']

    def parse(self, response):
        pass
