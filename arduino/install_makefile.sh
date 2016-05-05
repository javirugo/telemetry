#!/bin/bash

for i in `find . -maxdepth 1 -type d`
do
	[[ "$i" == "." ]] || [[ "$i" == "./lib" ]] && continue

	cd "$i"
	cp ../Makefile .
	rm -rf lib
	ln -sf ../lib .
	cd ..
done
