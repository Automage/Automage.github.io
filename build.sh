#!/bin/bash

clean() {
	rm writings/*
	echo "Emptied writings/ directory"
}

build() {
	echo "Building..."
	echo "Generating writings..."
	python3 scripts/gen_writings.py
	echo "Pushing to remote..."
	git add .
	git commit -m "Build at $(date)"
	git push
	echo "Done."
}

if [ "$1" == "clean" ]; then
	clean
else
	build
fi
