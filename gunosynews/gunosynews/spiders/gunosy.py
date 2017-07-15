# -*- coding: utf-8 -*-
import scrapy

from gunosynews.items import GunosynewsItem

#category9~42
class GunosySpider(scrapy.Spider):
    name = 'gunosy'
    allowed_domains = ['gunosy.com']
    
    start_urls = ["http://gunosy.com/categories/" + str(page) for page in range(1, 9)]#42
            

    def parse(self, response):
        category = response.xpath("//li[contains(@class, 'current')]/a/text()").extract_first()
        
        for cell in response.xpath("//div[@class='list_content']//div[@class='list_title']/a"):
            article = GunosynewsItem()
            article["title"] = cell.xpath("text()").extract_first()
            
            
            article["category"] = category
            
            
            detail_link = cell.xpath("@href").extract_first()
            request = scrapy.Request(detail_link, callback=self.parse_detail)
            
            request.meta["article"] = article
            
            yield request          
            
        #next_page = response.xpath("//div[@class='pager-link-option']/a/@href")
        #if next_page:
        #    url = response.urljoin(next_page[0].extract())
        #    yield scrapy.Request(url, callback=self.parse)
            
    def parse_detail(self, response):
        paragraphs = response.xpath("//div[contains(@class, 'article_main')]/div[contains(@class, 'article')]/p/text()").extract()
        text = "".join(paragraphs)
        
        article = response.meta["article"]
        article["text"] = text
        yield article

 