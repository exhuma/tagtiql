#!/bin/bash
function clean {
   pushd .
   cd $1
   for f in *.html; do
      cat ${f} | sed -e "s/_static/static/g" -e "s/_sources/sources/g" > tmp.html && mv tmp.html ${f}
   done
   popd
}

clean .
clean utilities

mv _static static
mv _sources sources

