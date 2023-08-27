#!/bin/bash
dt=$(date +"%D %T")
lol="site update: ${dt}"

git --git-dir /home/synchronous/code/insanium/static/.git add .
git --git-dir /home/synchronous/code/insanium/static/.git commit -am "$lol" 
git --git-dir /home/synchronous/code/insanium/static/.git push origin master
