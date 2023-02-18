#!/usr/bin/env python3

import argparse
import random

parser = argparse.ArgumentParser(description='Generate a random code.')
parser.add_argument('--length', '-l', metavar='N', type=int, default=8,
		help='the length of the number (default: 8)')

args = parser.parse_args()
digits = args.length

fmt = '%0' + str(digits) + 'd'
upper = 9
for i in range(digits - 1) :
	upper = upper * 10 + 9

rnd = random.SystemRandom()
print(fmt % rnd.randint(0, upper))
