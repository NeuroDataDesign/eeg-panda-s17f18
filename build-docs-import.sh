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
