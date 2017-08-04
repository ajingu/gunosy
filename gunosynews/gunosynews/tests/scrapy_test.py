import os
import sys
import scrapy
import unittest
from unittest.case import TestCase
# add 'gunosy/gunosynews' directory to sys.path
dir_path = os.path.dirname
sys.path.append(os.path.abspath(dir_path(dir_path(dir_path(__file__)))))

from gunosynews.items import GunosynewsItem # noqa
from gunosynews.spiders.gunosy import GunosySpider # noqa
from gunosynews.utils.fake_response import fake_response # noqa


class MyTestCase(TestCase):
    """Unittest for the scrapy bot 'gunosy'"""
    def setUp(self):
        """Setup the spider."""
        self.spider = GunosySpider()

    def test_parse(self):
        """Parse a fake content list page."""
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
        """Parse a fake article page."""
        response = fake_response("test_article.html",
                                 "https://gunosy.com/articles/R5QcG")
        article = GunosynewsItem()
        response.meta["article"] = article

        item = self.spider.parse_detail(response).__next__()

        self.assertEqual(item["text"][:5], "剛力彩芽が")
        self.assertEqual(item["text"][-5:], "浦山信一）")
        self.assertEqual(item["category"], "エンタメ")


if __name__ == "__main__":
    unittest.main()
