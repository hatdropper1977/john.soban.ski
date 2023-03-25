#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

SITENAME = 'John Sobanski'
SITESUBTITLE = u'Artificial Intelligence in the Cloud'
SITEURL = 'https://john.soban.ski'
#SITEURL = 'http://52.54.218.55:8000'
HEADER_COVER = 'images/city5.png'
#COLOR_SCHEME_CSS = 'tomorrow.css'

# Old Universal Analytics (UA)
#GOOGLE_ANALYTICS = 'UA-72207340-3'

# New Google Analytics 4  (GA-4)
GOOGLE_ANALYTICS ='G-68ZKCSR3PQ'

CATEGORY_FEED_ATOM = None

NOINDEX_THIN_CONTENT = True

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

DEFAULT_PAGINATION = 25

AUTHORS_SAVE_AS = 'authors.html'

CATEGORY_URL = 'cat/{slug}.html'
CATEGORY_SAVE_AS = 'cat/{slug}.html'
CATEGORIES_SAVE_AS = 'categories.html'

TAG_SAVE_AS = 'tag/{slug}.html'
TAGS_SAVE_AS = 'tags.html'

AUTHORS_BIO = {
  "john-sobanski": {
    "name": "John Sobanski",
    "cover": "https://john.soban.ski/images/bsod_cropped.jpg",
    "image": "https://john.soban.ski/images/john_happy.png",
    "location": "Washington, DC",
    "bio": "Professional Degree (Engr.) and Masters of Science in Electrical Engineering from GWU.<p><img src=\'https://john.soban.ski/images/six_badges.png\' alt=\'Cert\'></p><p>Google Cloud Certified Professional Data Engineer License <a href=\'https://www.credential.net/4951d2ef-2828-4f00-876c-5c2cc9ae1ab0\'>ctUxjj</a> (February 26th 2020, Recertified February 26th 2022, expires February 26th 2024)</p><p>Elasticsearch Certified Engineer License <a href=\'https://certified.elastic.co/81ae38bb-4a1a-42e5-9b34-7e90cd0c9617#gs.8l8jf7\'>19690771</a> (June 22nd 2020, Recertified June 22nd 2022, expires June 24th 2024)</p><p>Scrum Master Certified <a href=\'https://bcert.me/bc/html/show-badge.html?b=pffgetkt\'</a> (June 25th 2020, Recertified June 25th 2022, expires June 25th 2024)</p><p>AWS License <a href=\'https://www.credly.com/badges/831f8eef-4840-4674-bf6e-9875abb8397c\'>R25L4B4K1FF1Q9WP</a> (July 1st 2016, Recertified June 29th 2018, May 22nd 2021, expires May 22nd 2024)</p><p>Rarible <a href=\'https://rarible.com/sobanski\'>Verified</a> (June 28th, 2021)</p><p>CompTIA <a href=\'https://www.credly.com/badges/ea22ce36-a52d-4a53-a65b-65dc98af3c77\'>A+ Certified</a> (January 31st 2001)</p>",
    "linkedin": "johnsobanski/",
    "github": "hatdropper1977",
    "twitter": "SkiSoban",
  }
}

#Comments
DISQUS_SITENAME = 'freshlex'
TWITTER_USERNAME = 'SkiSoban'

MENUITEMS = (
             ('Archives', '/archives.html'),
             ('Fork me on GitHub!', 'https://github.com/hatdropper1977/john.soban.ski'),
             ('AWS Architecture', '/cat/howto.html'),
             ('Coins', '/cat/coins.html'),
             ('Data Science', '/cat/data-science.html'),
             ('Protocols', '/cat/ietf.html'),
)

# To show the line numbers for code blocks
# Refer https://docs.getpelican.com/en/stable/settings.html?highlight=MARKDOWN#basic-settings
#MARKDOWN = {
#  'extension_configs': {
#    'markdown.extensions.codehilite': {'css_class': 'highlight', 'linenums': True},
#    'markdown.extensions.extra': {},
#    'markdown.extensions.meta': {},
#  },
#  'output_format': 'html5',
#}
