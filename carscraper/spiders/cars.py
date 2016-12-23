# -*- coding: utf-8 -*-
import scrapy


class CarsSpider(scrapy.Spider):
    """Spider of http://24auto.ru"""
    name = 'cars'
    start_urls = ['http://www.24auto.ru/board/cars/']

    base_url = 'http://www.24auto.ru/'

    def parse(self, response):
        selector = response.css('.board_table__row::attr(href)')
        # If page is list of cars, have to go to every car on page
        if len(selector):
            for link in selector:
                yield scrapy.Request(
                    url='{base_url}/{path}'.format(
                        base_url=self.base_url,
                        path=link.extract())
                    ,
                    callback=self.parse
                )
        else:
            entity = {}

            for i, block in enumerate(response.css('.card_table')):
                headers = block.css('th::text').extract()
                values = block.css('td::text').extract()

                if i == 3:
                    entity.update({
                        'additional_info': values[1]
                    })
                    continue

                entity.update(dict(zip(headers, values)))

            yield entity
