#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

SITENAME = 'John Sobanski'
SITESUBTITLE = u'Artificial Intelligence in the Cloud'
SITEURL = 'https://john.soban.ski'
#SITEURL = 'http://52.54.218.55:8000'
HEADER_COVER = 'images/city5.png'

GOOGLE_ANALYTICS ='G-68ZKCSR3PQ'

#CATEGORY_FEED_ATOM = None

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
    "bio": "Professional Degree (Engr.) and Masters of Science in Electrical Engineering from GWU.<p><img src=\'https://john.soban.ski/images/six_badges.png\' alt=\'Cert\'></p><p>Google Cloud Certified Professional Data Engineer License <a href=\'https://www.credly.com/badges/3af351b3-8e0d-43cb-9996-05f6e9d23e8e/public_url\'>8c3166d14fef49faa159a02158108f64</a> (February 26th 2020 - Recertified 2022, 2024 - expires February 26th 2026)</p><p>Elasticsearch Certified Engineer License <a href=\'https://certified.elastic.co/81ae38bb-4a1a-42e5-9b34-7e90cd0c9617#gs.8l8jf7\'>19690771</a> (June 22nd 2020, Recertified 2022, 2024 expires June 20th 2026)</p><p>Scrum Master Certified <a href=\'https://bcert.me/bc/html/show-badge.html?b=pffgetkt\'</a> (June 25th 2020, Recertified 2022, 2024 expires June 25th 2024)</p><p>AWS License <a href=\'https://www.credly.com/badges/831f8eef-4840-4674-bf6e-9875abb8397c\'>R25L4B4K1FF1Q9WP</a> (July 1st 2016 - Recertified 2018, 2021, 2024 - expires May 20th 2027)</p><p>Rarible <a href=\'https://rarible.com/sobanski\'>Verified</a> (June 28th, 2021)</p><p>CompTIA <a href=\'https://www.credly.com/badges/ea22ce36-a52d-4a53-a65b-65dc98af3c77\'>A+ Certified</a> (January 31st 2001)</p>",
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

STATIC_PATHS = ['assets']

EXTRA_PATH_METADATA = {
    'assets/ads.txt': {'path': 'ads.txt'},
    'assets/android-chrome-192x192.png': {'path': 'android-chrome-192x192.png'},
    'assets/apple-touch-icon.png': {'path': 'apple-touch-icon.png'},
    'assets/BingSiteAuth.xml': {'path': 'BingSiteAuth.xml'},
    'assets/brave-rewards-verification.txt' : {'path': '.well-known/brave-rewards-verification.txt'},
    'assets/create_sitemap.sh' : {'path': 'create_sitemap.sh'},
    'assets/favicon-16x16.png': {'path': 'favicon-16x16.png'},
    'assets/favicon-32x32.png': {'path': 'favicon-32x32.png'},
    'assets/favicon.ico': {'path': 'favicon.ico'},
    'assets/google7a6d79cc71b58757.txt': {'path': 'google7a6d79cc71b58757.html'},
    'assets/mstile-150x150.png': {'path': 'mstile-150x150.png'},
    'assets/robots.txt': {'path': 'robots.txt'},
    'assets/safari-pinned-tab.svg': {'path': 'safari-pinned-tab.svg'},
}
