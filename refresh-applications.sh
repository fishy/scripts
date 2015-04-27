#!/bin/sh

TMPFILE=deadbeef`openssl rand -hex 14`

touch /Applications/${TMPFILE}
rm /Applications/${TMPFILE}
