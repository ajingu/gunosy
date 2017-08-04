import scrapy


class GunosynewsItem(scrapy.Item):
    """Base class for all scraped items."""
    text = scrapy.Field()
    category = scrapy.Field()
