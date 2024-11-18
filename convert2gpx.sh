#!/bin/sh

input=$1
extension=${1##*.}
output=${1%.*}.gpx

case "$extension" in
  "tcx")
    input_format=gtrnctr
    ;;
  "fit")
    input_format=garmin_fit
    ;;
  *)
    echo "Unknown format ${input}"
    exit 1
    ;;
esac

echo "Converting from ${input} to ${output} in format ${input_format}..."
exec gpsbabel -i "$input_format" -o gpx -f "$input" -F "$output"
