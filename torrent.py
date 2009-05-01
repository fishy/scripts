#!/usr/bin/env python

import sys
import os
from types import StringType
# get bencode from http://pypi.python.org/pypi/BitTorrent-bencode/5.0.8
from bencode import bencode, bdecode, BTFailure

try :
	torrent = sys.argv[1]
except IndexError :
	print "Usage: \"%s <torrent_file> [tracker_url]\" to show torrent info (without tracker_url), or to add tracker(s)" % sys.argv[0]
	sys.exit()

size = os.stat(torrent).st_size
file = open(torrent, "rb")
data = file.read(size)
file.close()
info = bdecode(data)

if len(sys.argv) == 2 :
	print info
	sys.exit()

if 'announce-list' not in info :
	list = [info['announce']]
	for i in range(len(sys.argv)-2) :
		tracker = sys.argv[i+2]
		if tracker not in list :
			list.append(tracker)
	print list
	info['announce-list'] = [list]
else :
	list = info['announce-list'][0]
	if type(list) == StringType :
		list = [list]
	for i in range(len(sys.argv)-2) :
		tracker = sys.argv[i+2]
		if tracker not in list :
			list.append(tracker)
	print list
	info['announce-list'][0] = list

writedata = bencode(info)
file = open(torrent, "wb")
file.write(writedata)
file.close()
