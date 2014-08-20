BoarG
=====
Description
-----------
Boarg is a simple GUI for the Version control System boar (www.boarvcs.com). It works as a wrapper for boar's command line Interface.
It is intended to be platform independent and has been tested on Linux and Windows 7.

It is not yet feature complete, as it does not support all of boar’s command line options.

Already supported are the following functions:
- creating repositories
- creating sessions
- get the status of a workdir
- update a workdir
- commit changes within a workdir

Prerequisites
-------------
- Python - www.python.org/ (tested with Python 2.7 and Python 3.4)
- PySide - www.qt-project.org/wiki/PySide (tested with PySide 1.2.1)
- QT - www.qt-project.org/ (will be installed with PySide)
- boar - www.boarvcs.com/ (tested with Version from November 16th, 2012 and Trunk as of August 2014)

Run BoarG
---------
If your system is configured to automatically execute .py files, just double-click boarg.py. Else run
```
python boarg.py
```
from your command line within the BoarG directory.
