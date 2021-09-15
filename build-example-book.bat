
@echo off

call python .\pandoc-folder.py .\example-book\.pandoc-folder\pandoc-folder-epub.pfy

call python .\pandoc-folder.py .\example-book\.pandoc-folder\pandoc-folder-html.pfy

pause
