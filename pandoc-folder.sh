#!/usr/bin/bash

base_dir=$(dirname $0)

python "$base_dir/pandoc-folder.py"

echo
echo "Press a key to exit."
read

