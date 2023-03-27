#!/bin/bash
echo '<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" 
  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'
ls *.html | grep -iv 'index' | grep -iv with-tensorflow | grep -iv lte-and-beyond | grep -iv visual-guide-to-forward-error | grep -iv archives.html | grep -iv authors.html | grep -iv categories.html | grep -iv tags.html | while read HTML_NAME
do
  if echo $HTML_NAME | grep -qiv 'google'
    then
      echo "  <url> 
    <loc>https://john.soban.ski/$HTML_NAME</loc>"
      IMG_DIR_NAME=$(echo $HTML_NAME | cut -f1 -d'.' | tr '-' '_' | sed 's/flask_wtf/flask-wtf/' | sed 's/aws_identity_and_access_management_iam/via_AWS_Identity_and_Access_Management/')
      if ls images | grep -qi $IMG_DIR_NAME; then
        IMG_DIR_NAME=$(ls images | grep -i $IMG_DIR_NAME)
    #    echo $IMG_DIR_NAME
        ls images/$IMG_DIR_NAME/ |  while read IMG_NAME
        do
          echo "    <image:image>
      <image:loc>
        https://john.soban.ski/images/$IMG_DIR_NAME/$IMG_NAME
      </image:loc>
    </image:image>"
        done
      fi
      echo "  </url>"
  fi
done
echo "</urlset>"
