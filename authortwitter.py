#!/usr/bin/env python3
# AuthorTwitter
# By Tristan Bacon
# URL: https://github.com/tristanojbacon/authortwitter
# Grabs the Twitter username of a blog post's author by passing the URL

from lxml import html
import requests
from urllib.parse import urljoin
import urllib.parse as urlparse
import re

class AuthorTwitter:
    def  __init__(self):
        return None
    def parse_twitter_button(self, text):
        author = text.replace("Follow @", "")
        return author

    def parse_twitter_button_iframe(self, src):
        parsed = urlparse.urlparse(src)
        result = re.search('screen_name=(.*)([^&]*)', parsed.fragment)
        author = result.group(1).replace('&show_count=true&show_screen_name=true&size=m', '')
        return author

    def scrape_author_page(self, url):
        headers = {'user-agent': 'testcollect/0.0.1'}
        page = requests.get(url, headers=headers)
        code = html.fromstring(page.content)
        return code
    def search_meta(self, url, code):
        # List of blogs that use the 'twitter:creator' meta tag and the actual author's username
        twitter_creator_tagged = ['engadget.com', 'coindesk.com', 'conversionxl.com', 'blog.bufferapp.com', 'citylab.com', 'socialmediaexplorer.com', 'martech.zone', 'financemagnates.com', 'readwrite.com']
        while True:
            try:
                # Runs against blogs in the twitter_creator_tagged list if detected
                # Some authors may not have included their username (or even have Twitter) in their blog profile, so this could still return 'null'
                if any(domain in url for domain in twitter_creator_tagged):
                    author = code.cssselect('meta[name="twitter:creator"]')[0].get('content')
                # Blogs with their own attribution format
                elif 'venturebeat.com' in url:
                    author = code.cssselect('a.author-twitter')[0].text
                elif 'blog.hootsuite.com' in url:
                    author = code.cssselect('meta[name="twitter:creator"]')[0].get('content').replace("https://twitter.com/", "")
                elif 'entrepreneur.com' in url:
                    author = code.xpath('//aside[@class="byline"] //div[@class="social"] //a[starts-with(@href, "https://twitter.com")]')[0].get('href').replace("https://twitter.com/", "")

                elif 'techcrunch.com' in url:
                    author = code.cssselect('span.twitter-handle a')[0].text

                elif ('lifehacker.com' in url) or ('kinja.com' in url):
                    author = code.cssselect('a.author-bio__twitter')[0].get('href').replace("https://twitter.com/", "")

                elif 'theverge.com' in url:
                    author = code.cssselect('a.c-byline__twitter-handle')[0].text

                elif 'mashable.com' in url:
                    author_url = code.cssselect('span.byline span.author_name a')[0].get('href')
                    author_url = urljoin(url, author_url)
                    code = self.scrape_author_page(author_url)
                    author = code.cssselect('div.profile-networks a.network-badge-twitter')[0].get('href').replace("https://twitter.com/", "")

                elif 'contentmarketinginstitute.com' in url:
                    author = code.xpath('//div[@id="author_box"] //a[starts-with(@href, "https://twitter.com")]/text()')[0]

                elif 'socialmediatoday.com' in url:
                    author = code.cssselect('div.views-field-field-user-twitter-url a')[0].text

                elif 'fivethirtyeight.com' in url:
                    author = code.cssselect('div.mini-bio span.twitter-username')[0].text

                elif 'shopify.com' in url:
                    text = code.cssselect('div.about-the-author a.twitter-follow-button')[0].text
                    author = self.parse_twitter_button(text)

                elif 'thehackernews.com' in url:
                    author = code.cssselect('div.author-info-bio a.a-tw')[0].get('href').replace("https://twitter.com/", "")

                elif 'theregister.co.uk' in url:
                    author_url = code.cssselect('div.byline a[title="Read more by this author"]')[0].get('href')
                    author_url = urljoin(url, author_url)
                    code = self.scrape_author_page(author_url)
                    author = code.cssselect('div.columnist a.tweet_link')[0].get('href').replace("http://twitter.com/intent/user?screen_name=", "")

                elif 'marketingland.com' in url:
                    author = self.parse_twitter_button_iframe(code.cssselect('div.author-module iframe[id="twitter-widget-0"]')[0].get('src'))

                elif 'convinceandconvert.com' in url:
                    author = code.cssselect('div.written-by a.twitter-follow-button')[0].get('href').replace("https://twitter.com/", "")

                elif 'contently.com' in url:
                    author_url = code.cssselect('span.credits a')[0].get('href')
                    code = self.scrape_author_page(author_url)
                    author = code.cssselect('div.social-presenter a.icon-twitter')[0].get('href').replace("http://twitter.com/", "")

                elif 'blogs.cisco.com' in url:
                    author_url = code.cssselect('span.list_author a[rel="author"]')[0].get('href')
                    code = self.scrape_author_page(author_url)
                    author = code.cssselect('div#author_links a.author_twitter')[0].get('href')
                    author = author.replace("https://twitter.com/", "")
                    author = author.replace("https://www.twitter.com/", "")

                elif 'consumerist.com' in url:
                    author = code.cssselect('span.author a[class="twitter"]')[0].get('title')

                elif 'nakedsecurity.sophos.com' in url:
                    author = code.cssselect('div.entry-content a[class="twitter-follow-button"]')[1].get('href').replace("https://twitter.com/", "")

                elif 'medium.com' in url:
                    author_url = code.cssselect('div.postMetaHeader a')[0].get('href')
                    code = self.scrape_author_page(author_url)
                    author = code.cssselect('div.buttonSet--profile a[title="Twitter"]')[0].get('href').replace("https://twitter.com/", "")

                else:
                    author = 'null'
                break
            except IndexError:
                    author = 'null'
                    print("-> No author Twitter username detected")
                    break
        author = author.replace("@","")
        return author

    def extract_author(self, url):
        headers = {'user-agent': 'testcollect/0.0.1'}
        page = requests.get(url, headers=headers)
        code = html.fromstring(page.content)
        author = self.search_meta(url, code)
        return author
