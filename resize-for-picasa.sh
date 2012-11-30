#!/bin/sh

size=${1:-"2048x2048"}
prepend="resize_"
ext="jpg"
otherext="JPG"

for file in *.${otherext}; do
	if [ -f ${file} ]; then
		target=${file%.${otherext}}.${ext}
		echo "pre-renaming ${file} to ${target} ..."
		mv ${file} ${target}
	fi
done

for file in *.${ext}; do
	if [ -f ${file} ]; then
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
	fi
done
