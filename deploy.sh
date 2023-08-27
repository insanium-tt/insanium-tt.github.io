#!/bin/bash

dir="/home/synchronous/code/insanium/static/"
cd dir

dt=$(date +"%D %T")
lol="site update: ${dt}"

git --git-dir /home/synchronous/code/insanium/static/.git add /home/synchronous/insanium/static/*
git --git-dir /home/synchronous/code/insanium/static/.git commit -am "$lol" 
git --git-dir /home/synchronous/code/insanium/static/.git push origin master
