#!/usr/bin/env bash
ts=$(date "+%Y-%m-%d %H:%m:%S")

#python update_daily.py
git add .
cmd="git commit -m '$ts'"
eval $cmd
git commit -m ''
git push origin master