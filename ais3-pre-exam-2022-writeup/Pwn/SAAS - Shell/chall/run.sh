#!/bin/sh
cd /app
timeout 60 ./chall
if [ $? -eq 134 ]; then
    cat crash-flag.txt
fi
