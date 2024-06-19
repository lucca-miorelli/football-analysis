#!/bin/sh

if [ "$1" = "download" ]; then
    python /code/jobs/download_data.py
else
    python /code/app/app.py
fi
