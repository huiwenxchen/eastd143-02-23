"""
A Scrapy spider for scraping data 
"""
from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    """
    A Scrapy spider for scraping data
    """
    name = "quotes"

    start_urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
    ]

    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = f'quotes-{page}.html'
    #     Path(filename).write_bytes(response.body)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)
            #alternatively you can use the following
            yield response.follow(next_page, callback=self.parse)
        # or you can use the following
        # yield from response.follow_all(css='ul.pager a', callback=self.parse)
