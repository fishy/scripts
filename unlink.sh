#!/bin/sh

prefix=$1

if [ -z "$1" ]; then
	echo "Unlink the links under current directory that matches the regexp"
	echo "Usage: $0 <regexp>"
	echo "Example: $0 \"^/usr/local/texlive/\""
	exit 1
fi

for file in *; do
	if [ -L ${file} ]; then
		link=`readlink ${file}`
		rmlink=`echo "${link}" | grep "${prefix}"`
		if [ -n "${rmlink}" ]; then
			echo "going to unlink \"${file}\" that links to \"${link}\"..."
			unlink ${file}
		fi
	fi
done
