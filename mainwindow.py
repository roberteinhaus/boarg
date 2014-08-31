#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# BoarG - mainwindow.py
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

import os

from PySide import QtCore, QtGui

import gui_resources

class MainWindow(object):

    def setupUi(self, MainWindow):      
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(1000,740)
        MainWindow.setWindowIcon(QtGui.QIcon(':/icons/boarg.png'))
        
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        dirListBox = QtGui.QVBoxLayout()
        dirButtonBox = QtGui.QHBoxLayout()

        self.dirList = QtGui.QListWidget(self.centralwidget)
        self.dirList.setObjectName("dirList")
        self.dirList.setStyleSheet( "QListWidget::item { padding:5px }" );
        # this is a hack, to get the icon to the right (as icons are always in the front)
        self.dirList.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.dirList.setUniformItemSizes(True)
        self.dirList.setMinimumWidth(400)       

        self.dirAddButton = QtGui.QPushButton()
        self.dirAddButton.setIcon(QtGui.QIcon(':/icons/add.png'))
        self.dirEditButton = QtGui.QPushButton()
        self.dirEditButton.setIcon(QtGui.QIcon(':/icons/edit.png'))
        self.dirRemoveButton = QtGui.QPushButton()
        self.dirRemoveButton.setIcon(QtGui.QIcon(':/icons/remove.png'))

        dirButtonBox.addWidget(self.dirAddButton)
        dirButtonBox.addWidget(self.dirEditButton)
        dirButtonBox.addWidget(self.dirRemoveButton)
        dirListBox.addWidget(self.dirList)
        dirListBox.addLayout(dirButtonBox)

        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)

        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        rpol = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        rpol.setHorizontalStretch(1)
        self.textEdit.setSizePolicy(rpol)

        hbox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()      
        hbox.addLayout(dirListBox)
        hbox.addWidget(self.textEdit)
        vbox.addLayout(hbox)
        vbox.addWidget(self.progressBar)
        self.centralwidget.setLayout(vbox)

        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuBoar = QtGui.QMenu(self.menubar)
        self.menuBoar.setObjectName("menuBoar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionFolders = QtGui.QAction(MainWindow)
        self.actionFolders.setObjectName("actionFolders")
        self.actionFolders.setShortcut('Ctrl+F')
        self.actionFolders.setIcon(QtGui.QIcon(':/icons/folder.png'))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionClose.setShortcut('Ctrl+Q')
        self.actionClose.setIcon(QtGui.QIcon(':/icons/exit.png'))
        self.actionHelp = QtGui.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionHelp.setShortcut('F1')
        self.actionHelp.setIcon(QtGui.QIcon(':/icons/help.png'))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setIcon(QtGui.QIcon(':/icons/about.png'))

        self.actionStatus = QtGui.QAction(MainWindow)
        self.actionStatus.setObjectName("actionStatus")
        self.actionStatus.setShortcut('F5')
        self.actionStatus.setIcon(QtGui.QIcon(':/icons/status.png'))
                
        self.actionUpdate = QtGui.QAction(MainWindow)
        self.actionUpdate.setObjectName("actionUpdate")
        self.actionUpdate.setShortcut('F6')
        self.actionUpdate.setIcon(QtGui.QIcon(':/icons/update.png'))

        self.actionCommit = QtGui.QAction(MainWindow)
        self.actionCommit.setObjectName("actionCommit")
        self.actionCommit.setShortcut('F7')
        self.actionCommit.setIcon(QtGui.QIcon(':/icons/commit.png'))


        self.menuFile.addAction(self.actionFolders)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)

        self.menuBoar.addAction(self.actionStatus)
        self.menuBoar.addAction(self.actionUpdate)
        self.menuBoar.addAction(self.actionCommit)

        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuBoar.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.toolbar = MainWindow.addToolBar('Toolbar')
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.toolbar.addAction(self.actionStatus)
        self.toolbar.addAction(self.actionUpdate)
        self.toolbar.addAction(self.actionCommit)
        
        spc = QtGui.QWidget();
        spc.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.toolbar.addWidget(spc)
        
        loadingLabel = QtGui.QLabel()
        loadingLabel.setMinimumWidth(30)
        movie = QtGui.QMovie(":/icons/loader.gif")
        loadingLabel.setMovie(movie)
        movie.start()
        
        self.loading = self.toolbar.addWidget(loadingLabel)
        self.loading.setVisible(False)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def showHelpDialog(self, MainWindow):
        helpDialog = QtGui.QDialog(MainWindow)
        layout = QtGui.QVBoxLayout()
        helpText = QtGui.QTextEdit()
        helpText.setReadOnly(True)
        try:
            path = os.path.dirname(os.path.realpath(__file__))
            helpText.setText(open(path + os.sep + "README.md").read())
        except (OSError, IOError) as e:
            helpText.setText("Visit http://boarg.wbbu.de")
        okButton = QtGui.QPushButton("Ok")
        okButton.clicked.connect(helpDialog.close)
        layout.addWidget(helpText)
        layout.addWidget(okButton)
        helpDialog.setLayout(layout)
        helpDialog.setObjectName("helpDialog")
        helpDialog.setWindowTitle("Help")
        helpDialog.resize(500, 450)
        helpDialog.exec_()

    def showLicenseDialog(self, MainWindow):
        licenseDialog = QtGui.QDialog(MainWindow)
        layout = QtGui.QVBoxLayout()
        licenseText = QtGui.QTextEdit()
        licenseText.setReadOnly(True)
        try:
            path = os.path.dirname(os.path.realpath(__file__))
            licenseText.setText(open(path + os.sep + "LICENSE").read())
        except (OSError, IOError) as e:
            licenseText.setText("Licensed under the GNU GENERAL PUBLIC LICENSE Version 3 or newer."
                "<br/>See &lt;<a href=\"http://www.gnu.org/licenses/\">"
                "http://www.gnu.org/licenses/</a>&gt;")
        okButton = QtGui.QPushButton("Ok")
        okButton.clicked.connect(licenseDialog.close)
        layout.addWidget(licenseText)
        layout.addWidget(okButton)
        licenseDialog.setLayout(layout)
        licenseDialog.setObjectName("licenseDialog")
        licenseDialog.setWindowTitle("License")
        licenseDialog.resize(500, 450)
        licenseDialog.exec_()

    def showAboutDialog(self, MainWindow, version):
        aboutDialog = QtGui.QDialog(MainWindow)
        layout = QtGui.QVBoxLayout()
        aboutText = QtGui.QLabel()
        aboutText.setObjectName("aboutText")
        aboutText.setText("<div align=\"center\"><h1>BoarG %s</h1>"
            "<br/>BoarG is a simple GUI for the<br/>version control system boar.<br/>"
            "<a href=\"http://www.boarvcs.com\">www.boarvcs.com</a><br/><br/>"
            "<small>Copyright &copy;2014 - Robert Einhaus</small><br/><br/>"
            "<a href=\"http://boarg.wbbu.de\">boarg.wbbu.de</a><br/><br/><br/>"
            "This program comes with ABSOLUTELY NO WARRANTY.<br/>This is free software, and you"
            "are welcome to<br/>redistribute it under certain conditions.</div>" % version)
        layout.addWidget(aboutText)

        hbox = QtGui.QHBoxLayout()
        okButton = QtGui.QPushButton("Ok")
        okButton.clicked.connect(aboutDialog.close)
        licenseButton = QtGui.QPushButton("Show License")
        licenseButton.clicked.connect(lambda: self.showLicenseDialog(MainWindow))
        hbox.addWidget(okButton)
        hbox.addWidget(licenseButton)
        layout.addLayout(hbox)

        aboutDialog.setLayout(layout)
        aboutDialog.setObjectName("aboutDialog")
        aboutDialog.setWindowTitle("About")
        aboutDialog.resize(350, 250)
        aboutDialog.exec_()

    def showRemoveDirDialog(self, MainWindow):
        removeDirDialog = QtGui.QDialog(MainWindow)
        layout = QtGui.QVBoxLayout()
        removeDirText = QtGui.QLabel()

        selectedDirs = self.dirList.selectedItems()
        for dir in selectedDirs:
            dirStr = dir.text() + "\n\n"

        removeDirText.setText(
            "Are you sure you want to delete the following entries:\n\n" + dirStr
        )
        layout.addWidget(removeDirText)

        hlayout = QtGui.QHBoxLayout()
        yesButton = QtGui.QPushButton("Yes")
        yesButton.clicked.connect(removeDirDialog.accept)
        hlayout.addWidget(yesButton)

        noButton = QtGui.QPushButton("No")
        noButton.clicked.connect(removeDirDialog.reject)
        hlayout.addWidget(noButton)

        layout.addLayout(hlayout)
        removeDirDialog.setLayout(layout)
        removeDirDialog.setObjectName("removeDirDialog")
        removeDirDialog.setWindowTitle("Remove Directory")
        return removeDirDialog.exec_()

    def showExistingRepoDialog(self, MainWindow):
        newSessionDialog = QtGui.QDialog(MainWindow)
        layout = QtGui.QVBoxLayout()
        newSessionText = QtGui.QLabel()
        newSessionText.setText("The repository directory you chose is already a boar repository.\n"
            "Do you want to create a new session for this repository and import the data?")
        layout.addWidget(newSessionText)

        hlayout = QtGui.QHBoxLayout()
        yesButton = QtGui.QPushButton("Yes")
        yesButton.clicked.connect(newSessionDialog.accept)
        hlayout.addWidget(yesButton)

        noButton = QtGui.QPushButton("No")
        noButton.clicked.connect(newSessionDialog.reject)
        hlayout.addWidget(noButton)

        layout.addLayout(hlayout)
        newSessionDialog.setLayout(layout)
        newSessionDialog.setObjectName("existingRepoDialog")
        newSessionDialog.setWindowTitle("Existing Repository")
        return newSessionDialog.exec_()

    def showAskForNewSessionDialog(self, MainWindow):
        newSessionDialog = QtGui.QDialog(MainWindow)
        layout = QtGui.QVBoxLayout()
        newSessionText = QtGui.QLabel()
        newSessionText.setText("The directory you chose is not a boar working directory\n"
            "Do you want to create a new repository / session and import this data?")
        layout.addWidget(newSessionText)

        hlayout = QtGui.QHBoxLayout()
        yesButton = QtGui.QPushButton("Yes")
        yesButton.clicked.connect(newSessionDialog.accept)
        hlayout.addWidget(yesButton)

        noButton = QtGui.QPushButton("No")
        noButton.clicked.connect(newSessionDialog.reject)
        hlayout.addWidget(noButton)

        layout.addLayout(hlayout)
        newSessionDialog.setLayout(layout)
        newSessionDialog.setObjectName("newSessionDialog")
        newSessionDialog.setWindowTitle("New Session")
        return newSessionDialog.exec_()

    def showSessionDialog(self, MainWindow, dir, session = "", repo = "", ignore = ""):
        newSessionDialog = QtGui.QDialog(MainWindow)
        layout = QtGui.QGridLayout()
        vlayout = QtGui.QVBoxLayout()
        hlayout = QtGui.QHBoxLayout()

        dirLabel = QtGui.QLabel("Directory")
        layout.addWidget(dirLabel, 0, 0)
        sessionLabel = QtGui.QLabel("Session")
        layout.addWidget(sessionLabel, 1, 0)
        repoLabel = QtGui.QLabel("Repository")
        layout.addWidget(repoLabel, 2, 0)
        ignoreLabel = QtGui.QLabel("Ignore List")
        layout.addWidget(ignoreLabel, 3, 0, QtCore.Qt.AlignTop)
        
        dirInput = QtGui.QLineEdit(dir)
        dirInput.setReadOnly(True)
        dirInput.setEnabled(False)
        dirInput.setFixedWidth(400)
        layout.addWidget(dirInput, 0, 1)
        sessionInput = QtGui.QLineEdit()
        layout.addWidget(sessionInput, 1, 1)
        repoInput = QtGui.QLineEdit()
        layout.addWidget(repoInput, 2, 1)
        ignoreList = QtGui.QTextEdit()
        ignoreList.setObjectName("ignoreList")
        layout.addWidget(ignoreList, 3, 1)
        
        if session != "":
            sessionInput.setText(session)
            sessionInput.setEnabled(False)
            sessionInput.setReadOnly(True)
        else:
            sessionInput.setText(os.path.basename(os.path.normpath(dir)))

        if repo != "":
            repoInput.setText(repo)
            repoInput.setEnabled(False)
            repoInput.setReadOnly(True)

        if ignore != "":
            ignoreList.setText(ignore)
            
        okButton = QtGui.QPushButton("Ok")
        okButton.clicked.connect(newSessionDialog.accept)
        hlayout.addWidget(okButton)

        cancelButton = QtGui.QPushButton("Cancel")
        cancelButton.clicked.connect(newSessionDialog.reject)
        hlayout.addWidget(cancelButton)

        vlayout.addLayout(layout)
        vlayout.addLayout(hlayout)

        newSessionDialog.setLayout(vlayout)
        newSessionDialog.setObjectName("newSessionDialog")
        newSessionDialog.setWindowTitle("Create new Session")
        ret = newSessionDialog.exec_()
        return {
            "code":ret,
            "dir":dirInput.text(),
            "session":sessionInput.text(),
            "repo":repoInput.text(),
            "ignore":ignoreList.toPlainText()
        }
        

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate(
            "MainWindow",
            "BoarG",
            None,
            QtGui.QApplication.UnicodeUTF8
        ))
        self.menuFile.setTitle(QtGui.QApplication.translate(
            "MainWindow",
            "File",
            None,
            QtGui.QApplication.UnicodeUTF8
        ))
        self.menuBoar.setTitle(QtGui.QApplication.translate(
            "MainWindow",
            "Boar",
            None,
            QtGui.QApplication.UnicodeUTF8
        ))
        self.menuHelp.setTitle(QtGui.QApplication.translate(
            "MainWindow",
            "Help",
            None,
            QtGui.QApplication.UnicodeUTF8
        ))
        self.actionFolders.setText(QtGui.QApplication.translate(
            "MainWindow",
            "Folders",
            None,
            QtGui.QApplication.UnicodeUTF8
        ))
        self.actionClose.setText(QtGui.QApplication.translate(
            "MainWindow",
            "Close",
            None,
            QtGui.QApplication.UnicodeUTF8
        ))
        self.actionHelp.setText(QtGui.QApplication.translate(
            "MainWindow",
            "Help",
            None,
            QtGui.QApplication.UnicodeUTF8
        ))
        self.actionAbout.setText(QtGui.QApplication.translate(
            "MainWindow",
            "About",
            None,
            QtGui.QApplication.UnicodeUTF8
        ))
        self.actionStatus.setText(QtGui.QApplication.translate(
            "MainWindow",
            "Status",
            None,
            QtGui.QApplication.UnicodeUTF8
        ))
        self.actionUpdate.setText(QtGui.QApplication.translate(
            "MainWindow",
            "Update",
            None,
            QtGui.QApplication.UnicodeUTF8
        ))
        self.actionCommit.setText(QtGui.QApplication.translate(
            "MainWindow",
            "Commit",
            None,
            QtGui.QApplication.UnicodeUTF8
        ))
