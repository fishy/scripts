#!/usr/bin/python3

import sys
from Foundation import *
from ScriptingBridge import *

ab = SBApplication.applicationWithBundleIdentifier_("com.apple.AddressBook")

for person in ab.people():
    fname = person.firstName()
    pfname = person.phoneticFirstName()
    lname = person.lastName()
    plname = person.phoneticLastName()
    note = person.note()
    print("%s %s %s %s %s" % (fname, pfname, lname, plname, note))

    if pfname and plname:
	cname = lname + fname
	if note:
	    note = cname + "\n" + note
	else:
	    note = cname
	person.setPhoneticLastName_("")
	person.setPhoneticFirstName_("")
	person.setFirstName_(pfname)
	person.setLastName_(plname)
	person.setNote_(note)

print("Done.")

