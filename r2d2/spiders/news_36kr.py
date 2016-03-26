# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.loader import ItemLoader
from r2d2.items import NewsItem
from urlparse import urljoin


class News36krSpider(scrapy.Spider):
    name = "news_36kr"
    allowed_domains = ["36kr.com"]
    start_urls = (
        'http://www.36kr.com',
    )

    def parse(self, response):
        for x in response.xpath("//div[@class='articles J_articleList']//a[@class='title info_flow_news_title']/@href").extract():
            request = scrapy.Request(urljoin(response.url, x), self.parse_news)
            request.meta['url'] = urljoin(response.url, x)
            yield request

    def parse_news(self, response):
    	item = ItemLoader(item=NewsItem(), response=response)
    	item.add_value('url', response.url)
    	item.add_value('title', response.xpath("//h1[@class='single-post__title']/text()").extract()[0])
    	item.add_value('content', response.xpath("//section[@class='article']/p/text()").extract())

    	return item.load_item()
