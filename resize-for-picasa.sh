#!/bin/sh

size="2048x2048"
append="_resize"
ext="jpg"

for file in *.${ext}; do
	already=`echo "${file}" | grep "${append}"`
	if [ -n "${already}" ]; then
		echo "skipping ${file} ..."
	else
		target=${file%.${ext}}${append}.${ext}
		echo "resizing ${file} to ${target} ..."
		convert -resize ${size} ${file} ${target}
	fi
done
