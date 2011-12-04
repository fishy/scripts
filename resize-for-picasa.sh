#!/bin/sh

size="2048x2048"
prepend="resize_"
ext="jpg"

for file in *.${ext}; do
	already=`echo "${file}" | grep "${prepend}"`
	if [ -n "${already}" ]; then
		echo "skipping ${file} ..."
	else
		target=${prepend}${file}
		echo "resizing ${file} to ${target} ..."
		convert -resize ${size}\> ${file} ${target}
		echo "renaming ${target} to ${file} ..."
		mv ${target} ${file}
	fi
done
