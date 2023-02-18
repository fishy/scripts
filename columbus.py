#!/usr/bin/env python3

import sys
import re

line = sys.stdin.readline().strip()
if not line :
	sys.exit()
names = line.split(",")
for i in range(len(names)) : names[i] = names[i].strip(' \t\r\n\x00')

timere = re.compile(r'(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)')

print(r'<?xml version="1.0" encoding="UTF-8"?>')
print(r'<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1">')

waypoints = []

print(r'<trk>')
print(r'<trkseg>')
while 1 :
	line = sys.stdin.readline().strip()
	if not line : break
	fields = line.split(",")
	point = {}
	for i in range(len(fields)) :
		point[names[i]] = fields[i].strip(' \t\r\n\x00')
		if names[i] == "LATITUDE N/S" :
			str = point[names[i]]
			point[names[i]] = float(point[names[i]].strip('NS'))
			if str.rfind('S') != -1 : point[names[i]] = 0 - point[names[i]]
		elif names[i] == "LONGITUDE E/W" :
			str = point[names[i]]
			point[names[i]] = float(point[names[i]].strip('EW'))
			if str.rfind('W') != -1 : point[names[i]] = 0 - point[names[i]]
		elif names[i] == "HDOP" or names[i] == "VDOP" or names[i] == "PDOP" :
			try :
				point[names[i]] = float(point[names[i]])
			except ValueError :
				pass
	try :
		if point['HDOP'] <= 0 or point['HDOP'] >= 20 or point['VDOP'] <= 0 or point['VDOP'] >= 20 or point['PDOP'] <= 0 or point['PDOP'] >= 20 :
			continue
	except KeyError :
		pass

	# fix missed keys
	try :
		foo = point['HDOP']
	except KeyError :
		point['HDOP'] = 0
	try :
		foo = point['VDOP']
	except KeyError :
		point['VDOP'] = 0
	try :
		foo = point['PDOP']
	except KeyError :
		point['PDOP'] = 0
	try :
		foo = point['VALID']
	except KeyError :
		point['VALID'] = None
	try :
		foo = point['FIX MODE']
	except KeyError :
		point['FIX MODE'] = None

	point['fix'] = 'none'
	if point['VALID'] == 'DGPS' :
		point['fix'] = 'dgps'
	elif point['FIX MODE'] == '2D' :
		point['fix'] = '2d'
	elif point['FIX MODE'] == '3D' :
		point['fix'] = '3d'
	else :
		point['fix'] = 'none'
	del point['FIX MODE']
	del point['VALID']
	timestr = point['DATE'] + point['TIME']
	del point['DATE']
	del point['TIME']
	groups = timere.match(timestr)
	if groups :
		point['time'] = "20%s-%s-%sT%s:%s:%sZ" % (groups.group(1), groups.group(2), groups.group(3), groups.group(4), groups.group(5), groups.group(6))
	else :
		point['time'] = ""
	point['name'] = point['VOX']
	del point['VOX']
	if point['TAG'] == 'C' :
		point['name'] = "Waypoint #%d" % len(waypoints)
	if len(point['name']) > 0 : waypoints.append(point)
	print(r'<trkpt lat="%f" lon="%f"><time>%s</time><ele>%s</ele><course>%s</course><speed>%s</speed><fix>%s</fix><hdop>%f</hdop><vdop>%f</vdop><pdop>%f</pdop></trkpt>' % (
			point['LATITUDE N/S'], point['LONGITUDE E/W'], point['time'],
			point['HEIGHT'], point['HEADING'], point['SPEED'], point['fix'],
			point['HDOP'], point['VDOP'], point['PDOP']))
print(r'</trkseg>')
print(r'</trk>')

for point in waypoints :
	print(r'<wpt lat="%f" lon="%f"><name>%s</name><desc>%s</desc><time>%s</time><ele>%s</ele><course>%s</course><speed>%s</speed><fix>%s</fix><hdop>%f</hdop><vdop>%f</vdop><pdop>%f</pdop></wpt>' % (
			point['LATITUDE N/S'], point['LONGITUDE E/W'], point['name'], point['name'],
			point['time'], point['HEIGHT'], point['HEADING'], point['SPEED'], point['fix'],
			point['HDOP'], point['VDOP'], point['PDOP']))

print(r'</gpx>')
