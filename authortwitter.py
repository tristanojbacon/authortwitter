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
        twitter_creator_tagged = ['engadget.com', 'coindesk.com', 'conversionxl.com', 'blog.bufferapp.com', 'citylab.com', 'socialmediaexplorer.com', 'martech.zone']
        while True:
            try:
                # Runs against blogs in the twitter_creator_tagged list if detected
                # Some authors may not have included their username (or even have Twitter) in their blog profile, so this could still return 'null'
                if any(domain in url for domain in twitter_creator_tagged):
                    author = code.cssselect('meta[name="twitter:creator"]')[0].get('content')
                    break

                if 'venturebeat.com' in url:
                    author = code.cssselect('a.author-twitter')[0].text
                    break
                elif 'fastcompany.com' in url:
                    author = code.cssselect('meta[property="author"]')[0].get('content')
                    break
                elif 'entrepreneur.com' in url:
                    author = code.xpath('//aside[@class="byline"] //div[@class="social"] //a[starts-with(@href, "https://twitter.com")]')[0].get('href').replace("https://twitter.com/", "")
                    break
                elif 'techcrunch.com' in url:
                    author = code.cssselect('span.twitter-handle a')[0].text
                    break
                elif 'lifehacker.com' in url:
                    author = code.cssselect('a.author-bio__twitter')[0].get('href').replace("https://twitter.com/", "")
                    break
                elif 'theverge.com' in url:
                    author = code.cssselect('a.c-byline__twitter-handle')[0].text
                    break
                elif 'contentmarketinginstitute.com' in url:
                    author = code.xpath('//div[@id="author_box"] //a[starts-with(@href, "https://twitter.com")]/text()')[0]
                    break
                elif 'socialmediatoday.com' in url:
                    author = code.cssselect('div.views-field-field-user-twitter-url a')[0].text
                    break
                elif 'shopify.com' in url:
                    text = code.cssselect('div.about-the-author a.twitter-follow-button')[0].text
                    author = self.parse_twitter_button(text)
                    break
                elif 'theregister.co.uk' in url:
                    author_url = code.cssselect('div.byline a[title="Read more by this author"]')[0].get('href')
                    author_url = urljoin(url, author_url)
                    code = self.scrape_author_page(author_url)
                    author = code.cssselect('div.columnist a.tweet_link')[0].get('href').replace("http://twitter.com/intent/user?screen_name=", "")
                    break
                elif 'marketingland.com' in url:
                    author = self.parse_twitter_button_iframe(code.cssselect('div.author-module iframe[id="twitter-widget-0"]')[0].get('src'))
                    break
                elif 'convinceandconvert.com' in url:
                    author = code.cssselect('div.written-by a.twitter-follow-button')[0].get('href').replace("https://twitter.com/", "")
                    break
                elif 'contently.com' in url:
                    author_url = code.cssselect('span.credits a')[0].get('href')
                    code = self.scrape_author_page(author_url)
                    author = code.cssselect('div.social-presenter a.icon-twitter')[0].get('href').replace("http://twitter.com/", "")
                    break
                else:
                    print("-> Something went wrong")
                    author = 'null'
                    break
            except IndexError:
                    author = 'null'
                    print("-> No author Twitter username detected")
                    break
        if "@" in author:
            author = author.replace("@","")
        return author

    def extract_author(self, url):
        headers = {'user-agent': 'testcollect/0.0.1'}
        page = requests.get(url, headers=headers)
        code = html.fromstring(page.content)
        author = self.search_meta(url, code)
        return author
