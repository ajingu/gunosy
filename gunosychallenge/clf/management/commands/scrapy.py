# -*- coding: utf-8 -*-

import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Crawl and scrape news data"
    
    def run_from_argv(self, argv):
        self._argv = argv
        self.execute(no_color = False)

    def handle(self, *args, **options):
        os.chdir(os.path.abspath("../../../../gunosynews"))
        from scrapy.cmdline import execute
        execute(self._argv[1:])