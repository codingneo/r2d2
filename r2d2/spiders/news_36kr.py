# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.loader import ItemLoader
from r2d2.items import NewsItem
from dateutil import parser
from pytz import timezone
from datetime import datetime, timedelta
from urlparse import urljoin


class News36krSpider(scrapy.Spider):
    name = "news_36kr"
    allowed_domains = ["36kr.com"]
    start_urls = (
        'http://www.36kr.com',
    )

    def parse_page(self, lasthour, response):
    	current = timezone("Singapore").localize(datetime.now())
    	earliest_time = current
    	
    	for x in response.xpath("//div[@class='articles J_articleList']//article"):
        	t = x.xpath("div//time[@class='timeago']/@title").extract()
        	publish_time = None
        	url = None
        	if len(t)>0:
        		publish_time = parser.parse(t[0])
        	if publish_time is not None:
        		if (publish_time<earliest_time):
        			earliest_time = publish_time

        		if (publish_time>lasthour):
        			url = x.xpath("div//a[@class='title info_flow_news_title']/@href").extract()[0]
        			if url is not None:
        				request = scrapy.Request(urljoin(response.url, url), self.parse_news)
            			request.meta['url'] = urljoin(response.url, url)
            			yield request

        if (earliest_time>lasthour):
        	loadmore_url = response.xpath("//div[@class='articles J_articleList']//a[@class='load-more J_listLoadMore']/@href").extract()[0]
        	request = scrapy.Request(urljoin(response.url, loadmore_url), self.parse_list)
        	request.meta['lasthour'] = lasthour
        	yield request


    def parse(self, response):
    	current = timezone("Singapore").localize(datetime.now())
    	lasthour = current - timedelta(hours = 8)

    	for request in self.parse_page(lasthour, response):
    		yield request

    def parse_list(self, response):
    	lasthour = response.meta['lasthour']

    	for request in self.parse_page(lasthour, response):
    		yield request


    def parse_news(self, response):
    	item = ItemLoader(item=NewsItem(), response=response)
    	item.add_value('url', response.url)
    	item.add_value('title', response.xpath("//h1[@class='single-post__title']/text()").extract()[0])
    	item.add_value('content', response.xpath("//section[@class='article']/p/text()").extract())

    	return item.load_item()
