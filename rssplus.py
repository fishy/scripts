#!/usr/bin/env python
# vim:et:ts=2:sw=2

import cgi, datetime, email.utils, json, re, time, urllib2

CONFIG_FILE = 'rssplus.config.json'
URL = 'https://www.googleapis.com/plus/v1/people/%s/activities/public?key=%s'

def error(msg):
  print('')
  print(msg + '.')
  exit(0)

def convertUtf8(data):
  if isinstance(data, unicode):
    return data.encode('utf-8')
  elif isinstance(data, dict):
    for key in data.keys():
      data[key] = convertUtf8(data[key])
  elif isinstance(data, list):
    for i in range(len(data)):
      data[i] = convertUtf8(data[i])
  return data

try:
  config = json.load(open(CONFIG_FILE))
except IOError:
  error('config file missing')
except ValueError:
  error('config file invalid')

try:
  key = config['key']
except KeyError:
  error('config file invalid')

form = cgi.FieldStorage()
if "id" not in form:
  error('"id" is required')
id = form.getfirst('id', None)

try:
  ids = config['ids']
  if not id in ids:
    error('id %s not whitelisted' % id)
except KeyError:
  # No whitelist, just allow everything.
  pass

if not re.match(r'^[0-9]*$', id):
  id = '+' + id
name = id

# HTTP header
print('Content-Type: application/xml; charset=UTF-8')
print('Content-Disposition: inline; filename="rss2.xml"')
print('')

# RSS header
print('<?xml version="1.0" encoding="utf-8"?>')
print('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
print('<channel>')
print('<docs>http://blogs.law.harvard.edu/tech/rss</docs>')
print('<link>https://plus.google.com/%s</link>' % id)

plus = convertUtf8(json.load(urllib2.urlopen(URL % (id, key))))

if len(plus['items']) > 0:
  name = cgi.escape(plus['items'][0]['actor']['displayName'])

print('<title>%s\'s G+ feed</title>' % name)
if "desc" in form:
  print('<description>%s</description>' % form.getfirst("desc", None))
else:
  print('<description>%s\'s G+ feed</description>' % name)

minl = max(0, int(form.getfirst('min', "2")) - 1)

# RSS items
for item in plus['items']:
  if item['verb'] != 'post':
    continue
  if item['provider']['title'] != 'Google+':
    continue

  url = item['url']

  date = item['published']
  date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
  date = email.utils.formatdate(time.mktime(date.timetuple()))

  obj = item['object']['content']
  lines = filter(None, obj.split('<br />'))
  if len(lines) <= minl:
    continue
  title = re.sub(r'\<.*?\>', '', lines[0])
  
  if 'attachments' in item['object'].keys():
    for att in item['object']['attachments']:
      t = att['objectType']
      link = None
      image = None
      if t == 'photo':
        img = att['fullImage']
        image = '<a href="%s"><img src="%s" height="%s" width="%s" /></a>' \
            % (att['url'], img['url'], img['height'], img['width'])
      elif t == 'article' or t == 'video':
        link = '<a href="%s">%s</a>' % (att['url'], att['displayName'])
        img = att['image']
        image = '<a href="%s"><img src="%s" height="%s" width="%s" /></a>' \
            % (att['url'], img['url'], img['height'], img['width'])
      elif t == 'album':
        link = '<a href="%s">%s</a>' % (att['url'], att['displayName'])
        img = att['thumbnails'][0]['image']
        image = '<a href="%s"><img src="%s" height="%s" width="%s" /></a>' \
            % (att['url'], img['url'], img['height'], img['width'])
      if link:
        obj = obj + '<br />' + link
      if image:
        obj = obj + '<br />' + image

  # RSS item
  print('<item>')
  print('<title>%s</title>' % title)
  print('<link>%s</link>' % url)
  print('<guid>%s</guid>' % url)
  print('<pubDate>%s</pubDate>' % date)
  print('<description><![CDATA[%s]]></description>' % obj)
  print('</item>')

# RSS footer
print('</channel>')
print('</rss>')
