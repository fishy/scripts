#!/usr/bin/env python

import sys, getpass, getopt
import hmac, hashlib, base64

lengths = [20]	# default value

optlist, args = getopt.getopt(sys.argv[1:], 'hl:', [ 'length=', 'help' ])

for opt in optlist :
	name, value = opt
	if (name == '-l') or (name == '--length') :
		lengths = value.split(',')
		for i in xrange(len(lengths)) :
			try :
				lengths[i] = int(lengths[i])
			except ValueError :
				sys.stderr.write('ERROR: \"%s\" is not a valid length arg.\n' % value)
				sys.exit(-1)
	elif (name == '-h') or (name == '--help') :
		print 'Usage:'
		print ' %s [-l|--length lengths] [sitekey]' % sys.argv[0]
		print ' %s -h|--help' % sys.argv[0]
		print
		print 'optional arguments:'
		print ' -h, --help\tshow this help message and exit'
		print ' -l, --length\tset a comma seperated output password length list, default=20'
		print ' sitekey\tthe main name of the domain (e.g. \"google\", \"facebook\", etc.)'
		print
		print 'tip:'
		print ' you can add the following line to your bashrc to set default lengths to 8, 10 & 20:'
		print '\talias onepwd=\"onepwd.py --length=8,10,20\"'
		print
		sys.exit(0)

try :
	msg = args[0]
except IndexError :
	sys.stderr.write('  sitekey: ')
	msg = sys.stdin.readline().rstrip()

key = getpass.getpass('masterkey: ', sys.stderr)
pwd = base64.b64encode(hmac.new(key, msg, hashlib.md5).digest()).rstrip('=').replace('+', '').replace('/', '')

sys.stderr.write('\n')
for length in lengths :
	sys.stdout.write('%4d: ' % length)
	sys.stdout.write(pwd[:length])
	sys.stdout.write('\n')
	sys.stdout.flush()
