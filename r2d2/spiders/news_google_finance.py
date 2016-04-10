# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from collections import Counter
from scrapy.contrib.loader import ItemLoader
from googlefinance import getNews
from r2d2.items import NewsItem


class NewsGoogleFinanceSpider(scrapy.Spider):
    name = "news_google_finance"
    symbols = ['NASDAQ:PYPL', 'NYSE:SQ', 'NYSE:V', 'NYSE:MA']

    def start_requests(self):
    	for symbol in self.symbols:
    		#stock = getQuotes(symbol)
    		news = getNews(symbol)
    		for article in news:
    			if "hour" in article['d']:
    				yield scrapy.Request(article['u'], self.parse)

    def parse(self, response):
    	print "parse: ", response.url
    	title = response.xpath('//title/text()').extract()[0]
    	p_elements = response.xpath("//body//p")
    	p_elements = [node for node in p_elements 
    		if (not not node.xpath("./text()").extract()) and 
    			(not not ' '.join(node.xpath("..//p/text()").extract()).strip())]
    	parent_counts = Counter(
    		[' '.join(node.xpath("..//p/descendant::text()[not(parent::script)]").extract()).strip() 
    			for node in p_elements])
    	content = parent_counts.most_common()[0][0]
    	# content = ' '.join(response.xpath("//body//p//text()").extract()).strip()
    	item = NewsItem(url=response.url, title=title, content=content)
    	yield item
        
