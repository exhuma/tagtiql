#!/bin/bash
for f in *.html; do
   cat ${f} | sed -e "s/_static/static/g" > ${f}
done
mv _static static

