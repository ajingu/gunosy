# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    A command which collects the article data.

    Use this class if you want to crawl and scrape the article data.

    Several arguments affect behaviour.

    ``help``
        A short description of the command, which will be printed in
        help messages.

    ``crawl @botname``
        Run the bot which name is '@botname'.
    """
    help = "Crawl and Scrape the article data."

    def run_from_argv(self, argv):
        """Pass the argument vector to the 'handle' method."""
        self._argv = argv
        self.execute(no_color=False)

    def handle(self, *args, **options):
        """
        Run the bot which name is '@botname'.
        """
        os.chdir(os.path.abspath("../gunosynews"))
        from scrapy.cmdline import execute
        execute(self._argv[1:])
