#!/usr/bin/env -S uv run --script
#
# /// script
# dependencies = ["bencoding"]
# ///

import sys
import os
# get bencode package from http://github.com/fishy/scripts/downloads
from bencoding import bencode, bdecode

try :
	torrent = sys.argv[1]
except IndexError :
	print("Usage: \"%s <torrent_file> [tracker_url]\" to show torrent info (without tracker_url), or to add tracker(s)" % sys.argv[0])
	sys.exit()

size = os.stat(torrent).st_size
file = open(torrent, "rb")
data = file.read(size)
file.close()
info = bdecode(data)

if len(sys.argv) == 2 :
	del info[b'info'][b'pieces']
	print(info)
	sys.exit()

if b'announce-list' not in info :
	list = [info[b'announce']]
	for i in range(len(sys.argv)-2) :
		tracker = [sys.argv[i+2].encode('utf-8')]
		if tracker not in list :
			list.append(tracker)
	print(list)
	info[b'announce-list'] = list
else :
	list = info[b'announce-list']
	for i in range(len(sys.argv)-2) :
		tracker = [sys.argv[i+2].encode('utf-8')]
		if tracker not in list :
			list.append(tracker)
	print(list)
	info[b'announce-list'] = list

writedata = bencode(info)
file = open(torrent, "wb")
file.write(writedata)
file.close()
