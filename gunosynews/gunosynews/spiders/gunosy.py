# -*- coding: utf-8 -*-
import scrapy
from gunosynews.items import GunosynewsItem


class GunosySpider(scrapy.Spider):
    """Spider that crawl and scrape articles."""
    name = 'gunosy'
    allowed_domains = ['gunosy.com']
    start_urls = [
        'http://gunosy.com/tags/' + str(page)
        for page in range(1, 2501)
    ]

    categories = {'エンタメ',
                  'スポーツ',
                  'おもしろ',
                  '国内',
                  '海外',
                  'コラム',
                  'IT・科学',
                  'グルメ'}

    def parse(self, response):
        """Parse a content list page.

        @url https://gunosy.com/tags/2
        @returns requests 0
        """
        detail_links = response.xpath(
            "//div[@class='list_content']//div[@class='list_title']//@href"
        ).extract()

        if detail_links:
            for detail_link in detail_links:

                article = GunosynewsItem()

                request = scrapy.Request(
                    detail_link, callback=self.parse_detail)

                request.meta['article'] = article

                yield request

            next_page = response.xpath(
                "//div[@class='pager-link-option']//@href"
            )

            if next_page:
                url = response.urljoin(next_page.extract_first())
                yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        """Parse an article page.

        @url https://gunosy.com/articles/RwrNu
        @returns items 0 1
        @scrapes category text
        """
        category = response.xpath(
            "//li[contains(@class, 'current')]/a/text()"
        ).extract_first()

        if category in self.categories:
            text = response.xpath(
                "string(//div[@class='article gtm-click']/.)"
            ).extract_first()

            article = response.meta['article']
            article['category'] = category
            article['text'] = text

            yield article
