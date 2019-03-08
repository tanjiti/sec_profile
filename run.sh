#!/usr/bin/env bash
ts=$(date "+%Y-%m-%d")

python update_daily.py
git add .
git commit -m '$ts'
git push origin master