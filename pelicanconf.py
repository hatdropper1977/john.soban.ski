#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

SITENAME = 'John Sobanski'
SITEURL = 'https://john.soban.ski'
#SITEURL = 'http://52.54.218.55:8000'
HEADER_COVER = 'images/elenabsl_shutterstock.jpg'
COLOR_SCHEME_CSS = 'monokai.css'

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

DEFAULT_PAGINATION = 10

CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

TAG_SAVE_AS = 'tag/{slug}.html'
TAGS_SAVE_AS = 'tags.html'

AUTHORS_BIO = {
  "john-sobanski": {
    "name": "John Sobanski",
    "cover": "https://john.soban.ski/images/bsod_cropped.jpg",
    "image": "https://john.soban.ski/images/sobanski.jpg",
    "website": "https://github.com/hatdropper1977/john.soban.ski",
    "location": "Washington, DC",
    "bio": "Electrical Engineer turned Cloud Architect.<p><img src=\'https://john.soban.ski/images/AWS_Badge.png\' alt=\'Cert\'></p><p>License <a href=\'https://aw.certmetrics.com/amazon/public/verification.aspx\'>R25L4B4K1FF1Q9WP</a> (July 1st 2016, Re-certified June 29th 2018)",
    "linkedin": "johnsobanski/",
    "github": "hatdropper1977",
  }
}

#Comments
DISQUS_SITENAME = 'freshlex'

MENUITEMS = (
             ('Fork me on GitHub!', 'https://github.com/hatdropper1977/john.soban.ski'),
             ('AWS Architecture', '/category/howto'),
             ('Coins', '/category/coins'),
             ('Data Science', '/category/data-science'),
             ('Protocols', '/category/ietf'),
)
