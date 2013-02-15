#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import re

AUTHOR = u'pelican-sample-site.com'
SITENAME = u'pelican-sample-site.com'
SITEURL = 'http://pelican-sample-site.com/blog'
BLOGURL = SITEURL
FEED_DOMAIN = "http://pelican-sample-site.com"
FEED_ATOM = "atom.xml"
FEED_RSS = "rss.xml"
FEED_ALL_ATOM = "atom.all.xml"
FEED_ALL_RSS = "rss.all.xml"

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Blogroll
LINKS =  (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
          ('Python.org', 'http://python.org'),
          ('Jinja2', 'http://jinja.pocoo.org'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 15

THEME = "bootstrap2"

# used to support templates outside the blog
PAGE = "blog"

PLUGINS = ['pelican.plugins.gravatar',]

STATIC_PATHS = ['images', 'media']


def popular_articles(articles):
    populars = [article for article in articles if hasattr(article, 'popularity')]

    def comparator(x, y):
        if x.popularity != y.popularity:
            return -1 * cmp(x.popularity, y.popularity)
        else:
            return -1 * cmp(x.date, y.date)

    return sorted(populars, cmp=comparator)


def media_url(url, site_root):
    if re.match("^https?://", "https://yahoo.com", re.IGNORECASE):
        return url
    else:
        return "%s/%s" %(site_root, url)


JINJA_FILTERS = {
    "popular_articles": popular_articles,
    "media_url": media_url,
}
