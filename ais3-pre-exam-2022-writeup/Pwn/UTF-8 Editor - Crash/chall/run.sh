#!/bin/sh
cd /app
timeout 60 ./chall
if [ $? -eq 139 ]; then
    cat crash-flag.txt
fi
