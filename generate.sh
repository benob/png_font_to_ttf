#!/bin/bash

for filename in bitmap_fonts/*.png; do
	width=`echo $filename | perl -ne '/(\d+)x(\d+)\.\w+$/ && {print "$1\n"}'`
	height=`echo $filename | perl -ne '/(\d+)x(\d+)\.\w+$/ && {print "$2\n"}'`
	echo $filename $width $height
	python png_font_to_ttf.py bitmap_fonts/`basename $filename .png`.woff $filename $width $height
done
