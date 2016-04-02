import scrapy
from googlefinance import getQuotes
from googlefinance import getNews
from scrapy.contrib.loader import ItemLoader
from r2d2.items import NewsItem
from scrapy.http.request import Request


class GooFinSpider(scrapy.Spider):
    name = "goo_fin"
    symbols = ['GOOG']

    def start_requests(self):
        for symbol in self.symbols:
            #stock = getQuotes(symbol)
            news = getNews(symbol)
            for article in news:
                yield Request(article['u'],self.parse)            

    def parse(self,response):
        print "parse: ", response.url
        item = NewsItem(url=response.url, title=response.xpath('//title/text()').extract(), 
            content=response.xpath('//body//p//text()').extract())
        yield item


 