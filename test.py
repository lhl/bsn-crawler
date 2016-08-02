#!/usr/bin/env python3

from bs4 import BeautifulSoup
import memcache
from   pprint import pprint
import requests


mc = memcache.Client(['127.0.0.1:11211'])

# TODO: Crawl Links on ME3MPD
# TODO: Crawl Search Results for my posts

# Get Page
html = mc.get('bsn-crawler.test')
url = 'https://forum.bioware.com/topic/266359-list-of-biotic-and-elemental-tech-combos/'
if not html:
  print('GETTING {}'.format(url))
  r = requests.get(url)
  html = r.text
  mc.set('bsn-crawler.test', html)
else:
  print('CACHED {}'.format(url))

# Parse DOM
soup = BeautifulSoup(html, 'html.parser')

### Pretty HTML
# print(soup.prettify())

print()

### Title
print('TITLE: {}'.format(soup.title.string))
print()

# Next
next_url = soup.find('link', {'rel':'next'})
print('NEXT: {}'.format(next_url['href']))
print()

### Last Page URL
last_url = soup.find('link', {'rel':'last'})
print('LAST: {}'.format(last_url['href']))
print()

### Author
author_url = soup.find('link', {'rel':'author'})
print('AUTHOR: {}'.format(author_url['href']))
print()

### Posts
posts = soup.findAll('div', {'class':'post_block'})
print('POSTS #:', len(posts))

post = posts[1]
print('POST 2 ({})'.format(post['id']))
print('===')
print('ID:', post.h3.a['data-entry-pid'])
print('PL:', post.h3.a['href'])
print('TITLE:', post.h3.a['title'])
print('DATE:', post.h3.find('abbr', {'class':'published'})['title'])
author = post.find('div', {'class':'author_info'})
print('AUTHOR:', author.span.string)
print('AVATAR:', author.img['src'])
print('BODY:', post.find('div', {'class':'post'}))
print('BODY_TEXT:', post.find('div', {'class':'post'}).text.strip())
innerHTML = ''.join([str(x) for x in post.find('div', {'class':'post'}).decode_contents(formatter='html')]).strip()
print('innerHTML:', innerHTML)



# Save to JSON

# Update Links
