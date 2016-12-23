# -*- coding: utf-8 -*-
import scrapy


class CarsSpider(scrapy.Spider):
    """Spider of http://24auto.ru"""
    name = 'cars'
    start_urls = ['http://www.24auto.ru/board/cars/']

    base_url = 'http://www.24auto.ru'

    def parse(self, response):
        selector = response.css('.board_table__row::attr(href)')
        # If page is list of cars, have to go to every car on page
        if len(selector):
            for link in selector:
                yield scrapy.Request(
                    url='{base_url}{path}'.format(
                        base_url=self.base_url,
                        path=link.extract()),
                    callback=self.parse
                )
            yield scrapy.Request(
                url='{base_url}/{path}'.format(
                    base_url=self.base_url,
                    path=response.css('.paging__next::attr(href)').extract()[0]
                ),
                callback=self.parse
            )
        else:
            entity = {}

            # Store general data
            for i, block in enumerate(response.css('.card_table')):
                headers = block.css('th::text').extract()
                values = block.css('td::text').extract()

                # Additional info is not matched to general pattern
                if i == 3:
                    entity.update({
                        'additional_info': values[1]
                    })
                    continue

                entity.update(dict(zip(headers, values)))

            # Store price
            entity.update({
                'price': int(''.join(
                    response.css('.card_block__price::text').extract()
                )[:-5])
            })

            # Store configuration

            configuration = {}

            for block in response.css('.card_configuration__group'):
                headers = block.css('h6::text').extract()
                values = []
                for ul in block.css('ul'):
                    values.append(ul.css('li::text').extract())

                configuration.update(dict(zip(headers, values)))

            entity.update({
                'configuration': configuration
            })

            yield entity
