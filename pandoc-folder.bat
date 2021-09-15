@echo off

set batch_dir=%~dp0

python %batch_dir%pandoc-folder.py %*
