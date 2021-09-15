# Pandoc-Folder

## Dependencies

1. python 3.9.7 or newer
2. pandoc 2.14.2 or newer

## Purpose

Run pandoc on all files with a given suffix in a folder and its
subfolders, to create one output document.

## Arguments

pandoc-folder.bat [path/to/book/.pandoc-folder/settings-file.yml]

### First Argument

The first argument is the filename, including path, of a
settings file.

By default, the suffix `.pfy` is used for the file. This is really
just a YAML file, but using a custom (and unused) extension allows
associating it with the `pandoc-folder.bat` file, in Windows.

This file is required to be under a sub-folder named `.pandoc-folder`.

The expected folder and file structure is like this:

```
book/
  .pandoc-folder/
    my-settings-file.pfy
```
  


## Settings File Format

The settings files are expected to be in [YAML](https://yaml.org/)
format.


## Example

To build the example book:

- on Windows, run: `.\build-example-book.bat`
- on Linux, run: `./build-example-book.sh`

To see how the example works, open one of these files with a text
editor, such as: Vim, Visual Studio Code, Nano, Notepad, etc.


## Configuration

The configuration file is `pandoc-folder-config.yml`. It is in
[YAML](https://yaml.org/) format.

Configuration options:

### pandoc_command: pandoc

The name of the pandoc command to run. Normally, just `pandoc`.

### require_settings_folder_name: .pandoc-folder

The name of the settings folder to require. If the 

### debug: False

Whether to print debug output. Useful for debugging/testing the
program, but prints too much for normal use.

### open_file_manager: False

Whether to open a file manager after the pandoc command is done.
This can be useful to show the output file. However, it can be
**really annoying** if you are running a batch which generates
*multiple output files, because a file manager window will be opened
*for each one!

### file_manager_exe: explorer

Which command to run to open the file manager. The default,
`explorer`, works under Windows. Under Linux, it will depend on which
distro and/or Window Manager, etc you are using.




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


