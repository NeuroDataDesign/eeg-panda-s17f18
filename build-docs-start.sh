#!/usr/bin/env bash
# build the lemur docs
cd docs/web/pkg
make clean
mkdir _static
make html
cd ..
# commit and push
git add -A
git commit -m "building and pushing docs"
git push origin master
cd ../../..
# switch branches and pull the data we want
git checkout gh-pages
# rm -rf ./*
echo 'Manually run rm -rf ./* in gh-pages'
