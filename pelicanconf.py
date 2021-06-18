#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

SITENAME = 'John Sobanski'
SITEURL = 'https://john.soban.ski'
#SITEURL = 'http://52.54.218.55:8000'
HEADER_COVER = 'images/elenabsl_shutterstock.jpg'
COLOR_SCHEME_CSS = 'monokai.css'

GOOGLE_ANALYTICS = 'UA-72207340-3'


PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

DEFAULT_PAGINATION = 25

CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

TAG_SAVE_AS = 'tag/{slug}.html'
TAGS_SAVE_AS = 'tags.html'

AUTHORS_BIO = {
  "john-sobanski": {
    "name": "John Sobanski",
    "cover": "https://john.soban.ski/images/bsod_cropped.jpg",
    "image": "https://john.soban.ski/images/john_happy.png",
    #"image": "https://john.soban.ski/images/sobanski-2.jpg",
    #"image": "http://52.54.218.55:8000/images/sobanski-2.jpg",
    #"website": "https://github.com/hatdropper1977/john.soban.ski",
    "location": "Washington, DC",
    "bio": "Professional Degree (Engr.) and Masters of Science in Electrical Engineering from GWU.<p><img src=\'https://john.soban.ski/images/four_badges.png\' alt=\'Cert\'></p><p>Google Cloud Certified Professional Data Engineer License <a href=\'https://www.credential.net/4951d2ef-2828-4f00-876c-5c2cc9ae1ab0\'>ctUxjj</a> (February 26th 2020 - 2022)</p><p>Elasticsearch Certified Engineer license <a href=\'https://certified.elastic.co/81ae38bb-4a1a-42e5-9b34-7e90cd0c9617#gs.8l8jf7\'>19690771</a> (June 22nd 2020 - 2022)</p><p>Scrum Master Certified <a href=\'http://bcert.me/spffgetkt\'>1238209</a> (June 25th 2020 - 2022)</p><p>AWS License <a href=\'https://www.youracclaim.com/badges/42379ff7-2298-48a0-ba32-c30198985295\'>R25L4B4K1FF1Q9WP</a> (July 1st 2016, Re-certified June 29th 2018, May 22nd 2021, expires May 22nd, 2024)</p>",
    "linkedin": "johnsobanski/",
    "github": "hatdropper1977",
    "twitter": "SkiSoban",
  }
}

#Comments
DISQUS_SITENAME = 'freshlex'
TWITTER_USERNAME = 'SkiSoban'

MENUITEMS = (
             ('Fork me on GitHub!', 'https://github.com/hatdropper1977/john.soban.ski'),
             ('AWS Architecture', '/category/howto'),
             ('Coins', '/category/coins'),
             ('Data Science', '/category/data-science'),
             ('Protocols', '/category/ietf'),
)
