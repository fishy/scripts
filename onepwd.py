#!/usr/bin/env python

import sys, getpass
import hmac, hashlib, base64

try :
	msg = sys.argv[1]
except IndexError :
	sys.stderr.write('  sitekey: ')
	msg = sys.stdin.readline().rstrip()

key = getpass.getpass('masterkey: ', sys.stderr)
pwd = base64.b64encode(hmac.new(key, msg, hashlib.md5).digest()).rstrip('=').replace('+', '').replace('/', '')

sys.stderr.write('\n')
sys.stdout.write(pwd[:20])
sys.stdout.flush()
sys.stderr.write('\n')
