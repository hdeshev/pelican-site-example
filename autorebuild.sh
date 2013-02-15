#!/bin/sh
# prerequisites:
# inotify-tools to detect filesystem changes
# libnotify-bin for Linux desktop notifications

rebuild() {
    notify-send "Rebuilding site..."
    fab build
}

rebuild

while inotifywait -r -e create,move,modify,delete --excludei "\.git|output" .
do
    rebuild
done
