#!/bin/sh

size="2048x2048"
prepend="resize_"
ext="jpg"
otherext="JPG"

for file in *.${otherext}; do
	target=${file%.${otherext}}.${ext}
	echo "pre-renaming ${file} to ${target} ..."
	mv ${file} ${target}
done

for file in *.${ext}; do
	already=`echo "${file}" | grep "${prepend}"`
	if [ -n "${already}" ]; then
		echo "skipping ${file} ..."
	else
		target=${prepend}${file}
		echo "resizing ${file} to ${target} ..."
		convert -resize ${size}\> "${file}" "${target}"
		echo "renaming ${target} to ${file} ..."
		mv "${target}" "${file}"
	fi
done
