#!/usr/bin/env python

import sys, os, re
import zipfile
import tempfile
import shutil

lang = "zh-CN"

tag = "xml:lang"
html_re = re.compile(r'(\<html[^\>]*)\>')
replace = r'\1 ' + tag + r'="' + lang + r'" >'

try :
	epub = sys.argv[1]
except IndexError :
	print "Usage: \"%s <filename.epub>\" to fix filename.epub, get filename.fix.epub" % sys.argv[0]
	sys.exit()

tmpdir = tempfile.mkdtemp()
logfile = os.fdopen(2, 'w')	# use stderr

def addZip(archive, base) :
	dirname = os.path.join(tmpdir, base)
	for f in os.listdir(dirname) :
		filename = os.path.join(base, f)
		fullname = os.path.join(tmpdir, filename)
		if os.path.isfile(fullname) :
			if f.lower().endswith("html") or f.lower().endswith("xml") :
				[tmpFile, tmpName] = tempfile.mkstemp()
				tmpFile = os.fdopen(tmpFile, 'w')
				htmlFile = open(fullname, 'r')
				for line in htmlFile.xreadlines() :
					if line.find(tag) == -1 :
						newline = html_re.sub(replace, line)
						if newline != line :
							logfile.write(filename + ":\n")
							logfile.write(line)
							logfile.write("->\n")
							logfile.write(newline)
							logfile.write("\n")
						line = newline
					tmpFile.write(line)
				tmpFile.close()
				os.remove(fullname)
				os.rename(tmpName, fullname)
			archive.write(fullname, filename)
		elif os.path.isdir(fullname) :
			addZip(archive, filename)

epubFile = zipfile.ZipFile(epub, "r")
epubFile.extractall(tmpdir)
epubFile.close()

epub = re.sub(r'(.*)\.epub', r'\1.fix.epub', epub)
epubFile = zipfile.ZipFile(epub, "w", zipfile.ZIP_DEFLATED)
addZip(epubFile, '.')
epubFile.close()

shutil.rmtree(tmpdir)

