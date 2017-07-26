import scrapy
import unittest
from unittest.case import TestCase
from gunosynews.spiders.gunosy import GunosySpider
from gunosynews.items import GunosynewsItem
from gunosynews.tests.fakeResponse import fake_response

class MyTestCase(TestCase):
    def setUp(self):
        self.spider = GunosySpider()

    def test_parse(self):
        response = fake_response("test_content_list.html")
        requests = self.spider.parse(response)

        self.assertTrue(requests)
        
        content_count = 0
        for request in requests:
            content_count += 1
            self.assertIsInstance(request, scrapy.Request)
            self.assertEqual(request.method, "GET")

            if content_count > 20:
                self.assertEqual("/".join(request.url.split("/")[:-1]),
                                 "https://gunosy.com/tags")

            else:
                self.assertEqual("/".join(request.url.split("/")[:-1]),
                                 "https://gunosy.com/articles")
        
        self.assertEqual(content_count, 21)

    def test_parse_detail(self):
        response = fake_response("test_article.html")
        article = GunosynewsItem()
        response.meta["article"] = article

        item = self.spider.parse_detail(response).__next__()

        self.assertIsNotNone(item["text"])
        self.assertEqual(item["category"], "エンタメ")

if __name__ == '__main__':
    unittest.main()
