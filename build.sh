#!/bin/bash

clean() {
	rm writing/*
	echo "Emptied writings/ directory"
}

push_remote() {
	echo "Pushing to remote..."
	git add .
	git commit -m "Build at $(date)"
	git push
}

build() {
	echo "Building..."
	echo "Generating writings..."
	python3 scripts/gen_writings.py
}

if [ "$1" == "clean" ]; then
	clean
elif [ "$1" == "nopush" ]; then
	clean
	build
	echo "Done."
else
	clean
	build
	push_remote
	echo "Done."
fi
