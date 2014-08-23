#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# BoarG - boarrunner.py
# Copyright (C) 2014 Robert Einhaus <robert@einhaus.info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import sys

from PySide import QtCore

class BoarRunner(QtCore.QThread):
    dataReady = QtCore.Signal(object)
    finished = QtCore.Signal(object)
    progress = QtCore.Signal(object)
    error = QtCore.Signal(object)
    exception = QtCore.Signal(object)
    
    def __init__(self, parent, cmd, path="", params=[]):
        QtCore.QThread.__init__(self, parent)
        self.cmd = cmd
        self.path = path
        self.params = params

    def addParam(self, param):
        self.params.append(param)

    def run(self):
        try:
            progress = 0
            isError = False
            infostr = 'Running boar ' + self.cmd + ' on ' + self.path
            self.dataReady.emit(infostr)
            processCmd = ["boar", self.cmd] + self.params
            if self.path != "": 
                p = subprocess.Popen(
                    processCmd,
                    cwd=self.path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:
                p = subprocess.Popen(
                    processCmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            progress += 5
            self.progress.emit(progress)
            i = 1
            ret = []
            while True:
                nextline = p.stdout.readline().decode(sys.stdout.encoding, "replace").strip()
                if nextline != "":
                    ret.append(nextline)
                    if ("Looking" in nextline or
                        "Verifying" in nextline or
                        "Scanning" in nextline or
                        "Sending" in nextline):
                        # Don't get multiple outputs for some keywords
                        nextline2 = nextline.splitlines()
                        nextline = nextline2[-1]
                if "ERROR" in nextline:
                    isError = True
                    error = nextline
                if p.poll() != None or nextline == '':
                    break
                self.dataReady.emit(nextline)
                if i == 1:
                    progress += 40
                elif i == 2:
                    progress += 40
                elif i == 3:
                    progress += 10
                else:
                    progress += 5
                i += 1
                self.progress.emit(progress)
            ret.append(self.cmd)
            if isError:
                self.error.emit(("boarerror", error))
                ret.append(error)
                ret.append("BOARERROR")
            self.progress.emit(100)
            self.finished.emit(ret)
        except OSError as err:
            self.exception.emit(("EXCEPTION: OSError", err.strerror))
