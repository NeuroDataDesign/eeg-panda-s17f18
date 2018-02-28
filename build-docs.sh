#!/usr/bin/env bash
# build the lemur docs
cd docs/web/pkg
make clean
make html
cd ..
# commit and push
git add -A
git commit -m "building and pushing docs"
git push origin master
cd ../../..
# switch branches and pull the data we want
git checkout gh-pages
rm -r ./*
touch .nojekyll
git checkout master docs/web/
mkdir pkg
mv ./docs/web/pkg/_build/html/* ./pkg/
mv ./docs/web/index.html ./
rm -rf ./docs
git add -A
git commit -m "publishing updated docs..."
git push origin gh-pages
# switch back
git checkout master
