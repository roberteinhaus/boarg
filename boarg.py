#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# BoarG - boarg.py
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

import json
import os
import sys
import threading

from PySide import QtCore, QtGui

from boarsession import BoarSession
from boarrunner import BoarRunner
from mainwindow import MainWindow

__version__ = "0.1.3"
_SESSIONCONFIGFILE = "config" + os.sep + "sessions"


class MainController(object):
    def __init__(self, parent=None):
        pass
        

class ControlMainWindow(QtGui.QMainWindow):
    '''Controller for boarg'''
    
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.sessions = []
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.connectUi()
        self.readConfig()
        self.loadDirList()

    def loading(self, isLoading):
        # Just show a nice gif animation and disable the input
        self.setEnabled(not isLoading)
        self.ui.loading.setVisible(isLoading)

    def writeConfig(self):
        try:
            sessionCfg = {}
            for id, session in enumerate(self.sessions):
                sessionCfg[id] = {
                    "path":session.path,
                    "session":session.session,
                    "repo":session.repo
                }
            with open(_SESSIONCONFIGFILE, 'w+') as file:
                file.write(json.dumps(sessionCfg, sort_keys=False, indent=4))
        except IOError:
            self.ui.statusbar.showMessage("Can't write config file", 3000)
        
    def checkConfig(self):
        try:
            if not os.path.exists(os.path.dirname(_SESSIONCONFIGFILE)):
                os.makedirs(os.path.dirname(_SESSIONCONFIGFILE))
            self.writeConfig()
            self.ui.statusbar.showMessage("Created empty config directory", 3000)
        except IOError:
            self.ui.statusbar.showMessage("Could not create config directory", 3000)

    def readConfig(self):
        try:
            with open(_SESSIONCONFIGFILE) as file:
                sessionCfg = json.load(file)
            for line in range(len(sessionCfg)):
                session = BoarSession(
                    sessionCfg[str(line)]["path"],
                    sessionCfg[str(line)]["session"],
                    sessionCfg[str(line)]["repo"]
                )
                self.sessions.append(session)
        except IOError:
            self.checkConfig()

    def loadDirList(self):
        currentRow = self.ui.dirList.currentRow()
        self.ui.dirList.clear()
        for session in self.sessions:
            item = QtGui.QListWidgetItem()
            item.setText(str(session))
            # Direction of the list ist set to rtl, to get the icon
            # to the right.  Therefore textlignment has to be set
            # to right, to get the text to the left ... strange.
            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            if session.status == BoarSession.MODIFIED:
                item.setIcon(QtGui.QIcon('icons/important.png'))
            elif session.status == BoarSession.UPTODATE:
                item.setIcon(QtGui.QIcon('icons/available.png'))
            elif session.status == BoarSession.UNKNOWN:
                item.setIcon(QtGui.QIcon('icons/unknown.png'))
            self.ui.dirList.addItem(item)
        #self.ui.dirList.setCurrentRow(currentRow)
    
    def removeDir(self):
        if self.ui.showRemoveDirDialog(self) == QtGui.QDialog.Accepted:
            selectedSession = self.ui.dirList.currentRow()
            self.sessions.pop(selectedSession)
            self.writeConfig()
            self.loadDirList()

    def folders(self):
        flags = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        dir = QtGui.QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            os.getcwd(),
            flags
        )
        self.addFolder(dir)

    def addFolder(self, dir):
        if dir != "":
            try:
                boarfile = open(dir + os.sep + ".boar" + os.sep + "info")
                boarCfg = json.load(boarfile)
                boarfile.close()
                findflags = QtCore.Qt.MatchStartsWith
                if self.ui.dirList.findItems(dir, findflags):               
                    return
                session = BoarSession(
                    dir,
                    boarCfg["session_name"],
                    boarCfg["repo_path"]
                )
                self.sessions.append(session)
                self.writeConfig()
                self.loadDirList()
                self.ui.dirList.setCurrentRow(self.ui.dirList.count() - 1)
            except IOError:
                self.askForNewSession(dir)

    def askForNewSession(self, dir):
        if self.ui.showAskForNewSessionDialog(self) == QtGui.QDialog.Accepted:
            self.newSession(dir)

    def aboutDialog(self):
        self.ui.showAboutDialog(self, __version__)

    def helpDialog(self):
        self.ui.showHelpDialog(self)

    def status(self):
        self.runCmd("status")

    def update(self):
        self.runCmd("update")

    def commit(self):
        self.runCmd("ci")

    def runCmd(self, cmd):
        path = self.getPath()
        if not path:
            return
        self.ui.textEdit.clear()
        self.runBoar(cmd, path)    
    
    def boarrunnerFinished(self, data):
        cmd = data.pop()
        selectedSession = self.ui.dirList.currentRow()
        item = self.ui.dirList.currentItem()
        if cmd == "ci":
            item.setIcon(QtGui.QIcon('icons/uptodate.png'))
        elif cmd == "status":
            datastr = "".join(data)
            if "M " in datastr or "A " in datastr or "D " in datastr:
                item.setIcon(QtGui.QIcon('icons/modified.png'))
            else:
                item.setIcon(QtGui.QIcon('icons/uptodate.png'))
        self.loading(False)
        self.sessions[selectedSession].buffer = self.ui.textEdit.toPlainText()
    
    def getPath(self):
        selectedSession = self.ui.dirList.currentRow()
        if selectedSession == -1:
            return ""
        return self.sessions[selectedSession].path

    def editSession(self):
        selectedSession = self.ui.dirList.currentRow()
        if selectedSession == -1:
            return
        params = [
            self.sessions[selectedSession].session,
            "ignore",
            "--repo=" + self.sessions[selectedSession].repo
        ]
        self.runBoar("getprop", "", params, self.getPropsFinished)

    def getPropsFinished(self, data):
        data.pop()
        ignoreList = '\n'.join(data)
        selectedSession = self.ui.dirList.currentRow()
        if selectedSession == -1:
            return
        self.loading(False)
        ret = self.ui.showSessionDialog(
            self,
            self.sessions[selectedSession].path,
            self.sessions[selectedSession].session,
            self.sessions[selectedSession].repo,
            ignoreList
        )
        if ret["code"] == QtGui.QDialog.Accepted:
            params = [
                self.sessions[selectedSession].session,
                "ignore",
                ret["ignore"],
                "--repo=" + self.sessions[selectedSession].repo
            ]
            self.runBoar("setprop", "", params, self.setPropsFinished)
                
    def setPropsFinished(self, data):
        self.loading(False)
                
    def newSession(self, dir):
        ret = self.ui.showSessionDialog(self, dir)
        if ret["code"] == QtGui.QDialog.Accepted:
            self.ui.textEdit.clear()
            self.loading(True)
            self.newSession = ret["session"]
            self.newRepo = ret["repo"]
            self.newDir = ret["dir"]
            self.ignore = ret["ignore"]
            self.runBoar("mkrepo", "", [self.newRepo], self.createRepoFinished)
                
    def askForExistingRepo(self):
        if self.ui.showExistingRepoDialog(self) == QtGui.QDialog.Accepted:
            self.createRepoFinished([""])

    def createRepoFinished(self, data):
        if data.pop() == "BOARERROR":
            self.askForExistingRepo()
        else:
            params = [self.newSession, "--repo=" + self.newRepo]
            self.runBoar("mksession", "", params, self.createSessionFinished)

    def createSessionFinished(self, data):
        if self.ignore != "":
            params = [self.newSession, "ignore", self.ignore, "--repo=" + self.newRepo]
            self.runBoar("setprop", "", params, self.importData)
        else:
            self.importData(data)

    def importData(self, data):
        params = [self.newDir, self.newSession, "--repo=" + self.newRepo]
        self.runBoar("import", "", params, self.importSessionFinished)

    def importSessionFinished(self, data):
        self.addFolder(self.newDir)
        item = self.ui.dirList.currentItem()
        item.setIcon(QtGui.QIcon('icons/uptodate.png'))
        self.loading(False)
    
    def get_data(self, data):
        line = self.formatLine(data)
        self.ui.textEdit.append(line)
        
    def handleError(self, error):
        self.ui.progressBar.setValue(0)
        print(error[0] + " - " + error[1])
        self.loading(False)
        
    def handleException(self, error):
        line = self.formatLine(error[0] + " - " + error[1])
        self.ui.progressBar.setValue(0)
        self.ui.textEdit.append(line)
        self.loading(False)

    def get_progress(self, data):
        self.ui.progressBar.setValue(data)
    
    def formatLine(self, line):
        if "M " in line:
            return '<b><span style="color:orange">' + line + '</span></b>'
        elif "A " in line:
            return '<b><span style="color:green">' + line + '</span></b>'
        elif "D " in line:
            return '<b><span style="color:red">' + line + '</span></b>'
        elif "ERROR" in line or "NOTICE" in line:
            return '<b>' + line + '</b>'
        elif "EXCEPTION" in line:
            return '<b><span style="color:red">' + line + '</span></b>'
        else:
            return line

    def selectSession(self, selectedSession):
        self.ui.textEdit.clear()
        self.ui.progressBar.setValue(0)
        try:
            lines = self.sessions[selectedSession].buffer.splitlines()
        except IndexError:
            return
        for line in lines:
            self.ui.textEdit.append(self.formatLine(line))

    def runBoar(self, command, path="", params=[], callback=None):
        self.loading(True)
        if callback is None:
            callback = self.boarrunnerFinished
        self.boarRunner = BoarRunner(self, command, path, params)
        self.boarRunner.dataReady.connect(self.get_data, QtCore.Qt.QueuedConnection)
        self.boarRunner.finished.connect(callback, QtCore.Qt.QueuedConnection)
        self.boarRunner.progress.connect(self.get_progress, QtCore.Qt.QueuedConnection)
        self.boarRunner.error.connect(self.handleError, QtCore.Qt.QueuedConnection)
        self.boarRunner.exception.connect(self.handleException, QtCore.Qt.QueuedConnection)
        self.boarRunner.start()

    def connectUi(self):
        self.ui.actionFolders.triggered.connect(self.folders)
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.aboutDialog)
        self.ui.actionHelp.triggered.connect(self.helpDialog)
        self.ui.actionStatus.triggered.connect(self.status)
        self.ui.actionUpdate.triggered.connect(self.update)
        self.ui.actionCommit.triggered.connect(self.commit)
        self.ui.dirAddButton.clicked.connect(self.folders)
        self.ui.dirRemoveButton.clicked.connect(self.removeDir)
        self.ui.dirEditButton.clicked.connect(self.editSession)
        self.ui.dirList.currentRowChanged.connect(self.selectSession)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())
