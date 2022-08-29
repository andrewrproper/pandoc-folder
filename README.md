# Pandoc-Folder

![folder icon](img/icons/Alumin/1472849908_Documents_4--128x128.png)

## Version

0.1.0 - initial release

### Changelog

See [CHANGES.md](CHANGES.md)


## License

[GPL v3](./LICENSE) 
- [summary](https://choosealicense.com/licenses/gpl-3.0/#)
- [official site](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Dependencies

1. [python](https://www.python.org/) 3.9.7 or newer
2. [pandoc](https://pandoc.org/) 2.14.2 or newer

## Installation

### 1. Install module dependencies (global option)

There are only a small number of dependencies to be installed.

On a command line, navigate to the folder and run:

```
pip3 install -r requirements.txt
```

And that will install all required dependencies, globally.


### 2. Installing to local folder only

This is possible using [venv](https://docs.python.org/3/library/venv.html). 

However, this is currently not supported by the batch files included
with `pandoc-folder`.

## Purpose

Run pandoc on all files with a given suffix in a folder and its
subfolders, to create one output document.

For example, it will find all markdown files in a directory and its
subdirectories, and use pandoc to create one output file from them.

This can be used to write an ebook in multiple markdown files, then
generate a single EPUB or HTML document which includes the content
from all of them.

## Usage

```
python pandoc-folder.py ./path/to/book/.pandoc-folder/settings-file.yml
```

Or, with Windows batch file:

```
pandoc-folder.bat ./path/to/book/.pandoc-folder/settings-file.yml
```

Or, with bash script:

```
pandoc-folder.sh ./path/to/book/.pandoc-folder/settings-file.yml
```

If you add the Pandoc-Folder folder into your `PATH`, then you can run
the batch/bash commands on the command-line, from any folder.

## Arguments

The first argument is the filename, including path, of a
settings file.

### Settings File Suffix

By default, the suffix `.pfy` is used for the file. This is really
just a YAML file, but using a custom (and unused) extension allows
associating it with the `pandoc-folder.bat` file, in Windows.

`.pfy` is short for **"Pandoc-Folder YAML"**.

### Required Folder Structure

Any settings file is required to be under a sub-folder named
`.pandoc-folder`.  This sub-folder can be used to store all settings
files. See the `example-book/.pandoc-folder` folder for an example.
This keeps the files organizes, so that the files related to pandoc
aren't mixed with your source files.

Note that under Linux, the `.pandoc-folder` folder will not be shown
by default. It will be considered a hidden folder, because it starts
with a period (`.`). However, it is common to store settings in a
folder starting with a period under Linux. Hopefully, this won't be a
problem. If it is, **you can change the folder name in the
configuration**. Or use the `-a` flag for the `ls` command, to see all
folders, including hidden ones.

### Expected Folder and File Structure

The expected folder and file structure is like this:

```
./book/
  .pandoc-folder/
    my-settings-file.pfy
```

See the `example-book/.pandoc-folder` folder for an example of how
the files are laid out.


### What Pandoc Command Does This Run?

Here is an example of part of the output, when Debug is set to True in
the config. This shows the pandoc command used when building the
example ebook. You can see that the input files, ending in `.md`, are
the last arguments. Also, they are found regardless of whether they
are in subfolders under the `example-book` folder.

```
DEBUG - === pandoc_command:
('pandoc --css="example-book\\.pandoc-folder\\pandoc-epub.css" '
 '--metadata-file="example-book\\.pandoc-folder\\pandoc-meta.yml" '
 '--defaults="example-book\\.pandoc-folder\\pandoc-defaults-epub.yml" -o '
 '"out-pandoc\\example-book.epub" "example-book\\part-1.md" '
 '"example-book\\part 2\\00 section.md" "example-book\\part 2\\sub-part 1.md" '
 '"example-book\\part 2\\sub-part 2.md"')
DEBUG - ===
```

## Associating Pandoc-Folder to the `.pfy` File Type in Windows

By default, the suffix `.pfy` is used for the settings file. This are
really just YAML files, but using a custom (and unused) extension
allows associating it with the `pandoc-folder.bat` file, in Windows.

To associate the file under Windows: 

1. browse it in Windows Explorer (file manager). 
2. Click on it to select it. 
3. Then, hold down a shift key while right-clicking on the file. 
4. In the right-click menu that comes up, you should see an 
   `Open With` option. Click it.
5. In the dialog that appears, click "More Apps"
6. Scroll to the bottom of the list of apps
7. Click "Look for another App on this PC"
8. Browse to the `pandoc-folder` folder
9. Select `pandoc-folder.bat`
10. Click the `Open` button.

After doing this, whenever you double-click on a `.pfy` file in
Windows Explorer, it will run the `pandoc-folder.bat`. This will run
the pandoc-folder python program on that file, and then wait for you
to press a key before it closes the terminal.




## Settings File Format

The settings files are expected to be in [YAML](https://yaml.org/)
format.

### pandoc_defaults_file: pandoc-defaults-html.yml

Optional: specify a defaults file for pandoc to use.  This is a useful
way to provide a number of default values for pandoc options, without
needing to specific them on the command-line.

This file should be found in the same folder as the settings file.

### pandoc_meta_file: pandoc-meta.yml

Optional: specify a metadata file for pandoc to read. This can be used to specify the title, author, and other fields for the book/document.

This file should be found in the same folder as the settings file.

### pandoc_css_file

Optional: specify a CSS file for pandoc to use when formatting the
output book. Useful for EPUB or HTML output, and possibly others.

This file should be found in the same folder as the settings file.

### source_files_suffix: `md`

This suffix is used to find the source files. So, for a suffix of
`md`, Pandoc-Folder will find all `*.md` files in the directory or
subdirectories. These will all be passed to pandoc as input files.

The default suffix is `md`, for converting markdown files. However,
you could change this to another suffix that pandoc recognizes, such
as `docx`.

### out_file_rel

This is an array of the directory and subdirectories up to and
including the output file.

If the output path doesn't exist, it will be created.




## Example of Using Pandoc-Folder

To build the example book:

- on Windows, run: `.\build-example-book.bat`
- on Linux, run: `./build-example-book.sh`

To see how the command for building th example book works, open one of
these files with a text editor (such as: Visual Studio Code, Vim,
Nano, Notepad, etc.)


## Configuration

The configuration file is `pandoc-folder-config.yml`. It is in
[YAML](https://yaml.org/) format.

Configuration options:

### pandoc_command: `pandoc`

The name of the pandoc command to run. Normally, just `pandoc`.

### require_settings_folder_name: `.pandoc-folder`

The name of the settings folder to require. If the 

### debug: `False`

Whether to print debug output. Useful for debugging/testing the
program, but prints too much for normal use.

### open_file_manager: `False`

Whether to open a file manager after the pandoc command is done.
This can be useful to show the output file. However, it can be
**really annoying** if you are running a batch which generates
*multiple output files, because a file manager window will be opened
*for each one!

### file_manager_exe: `explorer`

Which command to run to open the file manager. The default,
`explorer`, works under Windows. Under Linux, it will depend on which
distro and/or Window Manager, etc you are using.




