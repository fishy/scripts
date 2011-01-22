#!/usr/bin/env python

import sys, os, re
import zipfile
import tempfile
import shutil

lang = "zh-CN"

skip_keyword = "xml:lang"
html_re = re.compile(r'(\<html[^\>]*)\>')
replace = r'\1 xml:lang="' + lang + r'" >'

try :
	epub = sys.argv[1]
except IndexError :
	print "Usage: \"%s <filename.epub>\" to fix filename.epub, get filename.fix.epub" % sys.argv[0]
	sys.exit()

tmpdir = tempfile.mkdtemp()

def addZip(archive, base) :
	dirname = os.path.join(tmpdir, base)
	for f in os.listdir(dirname) :
		filename = os.path.join(base, f)
		fullname = os.path.join(tmpdir, filename)
		if os.path.isfile(fullname) :
			if f.lower().endswith("html") or f.lower().endswith("xml") :
				[tmpfile, tmpfilename] = tempfile.mkstemp()
				tmpfile = os.fdopen(tmpfile, 'w')
				htmlFile = open(fullname, 'r')
				for line in htmlFile.xreadlines() :
					if line.find(skip_keyword) == -1 :
						newline = html_re.sub(replace, line)
						if newline != line :
							print filename + ":\n" + line + newline
						line = newline
					tmpfile.write(line)
				tmpfile.close()
				os.remove(fullname)
				os.rename(tmpfilename, fullname)
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

#print tmpdir
shutil.rmtree(tmpdir)

