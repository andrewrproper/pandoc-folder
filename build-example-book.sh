#!/usr/bin/bash

echo
python pandoc-folder.py ./example-book/.pandoc-folder/pandoc-folder-epub.pfy
echo

echo
python pandoc-folder.py ./example-book/.pandoc-folder/pandoc-folder-html.pfy
echo

echo
echo "Press a key to exit."
read

