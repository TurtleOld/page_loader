### Hexlet tests and linter status:

[![Actions Status](https://github.com/TurtleOld/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/TurtleOld/python-project-lvl3/actions)

### Project tests and linter status:

[![Actions Status](https://github.com/TurtleOld/python-project-lvl3/workflows/page-loader/badge.svg)](https://github.com/TurtleOld/python-project-lvl3/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/28e202a8b1e8a675b74c/maintainability)](https://codeclimate.com/github/TurtleOld/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/28e202a8b1e8a675b74c/test_coverage)](https://codeclimate.com/github/TurtleOld/python-project-lvl3/test_coverage)

# Welcome to project "Page loader".

##### _This is the third [Hexlet](https://ru.hexlet.io) platform project written in Python programming language_

### This library allows you to download web pages

> Minimum requirements to launch the package:
>
> Ubuntu 20.04+. Installation and operation of the package in other operating systems are not guaranteed.

> The package is able to work with both relative and absolute paths to files

### To install the package

    python -m pip install git+https://github.com/TurtleOld/python-project-lvl3

### How to use the package - page-loader -h

    usage: page-loader [options] <url>

    Internet page loader
    
    positional arguments:
      url
    
    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            output dir (default "current directory")
      -v, --version         show program's version number and exit

## Demonstration of capabilities of this package

### The main work of the program

[![asciicast](https://asciinema.org/a/481021.svg)](https://asciinema.org/a/481021)

### In case of errors in the spelling of the path or link, appropriate warnings will be displayed:
[![asciicast](https://asciinema.org/a/481022.svg)](https://asciinema.org/a/481022)