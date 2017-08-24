# `gitpitch-generate`
A tool for generating groups of related presentations using GitPitch quickly and easily.

## Synopsis
This tool will automatically look for source Markdown and optionally corresponding
YAML files in the "assets/src" directory (relative to the current working directory), or 
you can specify a custom source directory with the `--src-dir` option.

Source Markdown files will be transferred to the output directory (the current working
directory or the directory supplied by the `--output-dir` option) as directories containing
a PITCHME.md file (and optionally the corresponding PITCHME.yaml) as required by GitPitch.

An "index" slide will be created in the top level direcotry of your output directory.  
The index slide will contain auto-generated links to each of your presentations.

You can specify the same YAML file for all presentations by supplying a "common.yaml" file
in the source directory; custom YAML files that are named to match their corresponding 
Markdown file will override this default file.

You can also supply a custom YAML file for the index slide by including a file named
"index.yaml" in the source directory.

All other assets (images and custom css) should be stored in the corresponding
directories under "assets/" as required by GitPitch (this tool is agnostic of these
files).

Finally, the tool will automatically add all changes to your git repository and initiate
a git commit for you when it finishes, unless you specify the `--no-git` flag.  You 
can also initiate a push to your remote repository by adding the `--push` flag.

Enjoy!

## Installation
Currently this is just a standalone Python script, so you can simply run it:

```bash
python gitpitch-generate.py
```

Or, you can "install" it by placing it somewhere on your system and creating an alias
or a symlink (or similar) in a system directory; for example (UNIX/Linux/Mac OS):

```bash
chmod +x /wherever/you/placed/gitpitch-generate.py
ln -s /wherever/you/placed/gitpitch-generate.py /usr/local/bin/gitpitch-generate
```

## Usage

```text
gitpitch-generate [-h] [--src-dir source_directory]
                  [--output-dir output_directory] [--no-git | --push]

optional arguments:
  -h, --help            show this help message and exit
  --src-dir source_directory
                        Directory containing Markdown and YAML source files for each presentation.
  --output-dir output_directory
                        Top-level directory where the main presentation index and sub-presentations will be placed.
  --no-git              Do not perform any `git` operations after generating the file heirarchy.
  --push                Automatically initiate a `git push` after generating and committing the changes.
```
