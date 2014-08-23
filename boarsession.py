#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# BoarG - boarsession.py
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

class BoarSession(object):
    UNKNOWN=0
    UPTODATE=1
    MODIFIED=2

    def __init__(self, path, session="", repo=""):
        self.path = path
        self.session = session
        self.repo = repo
        self.buffer = ''
        self.status = self.UNKNOWN

    def boarCommit(self):
        pass

    def boarStatus(self):
        pass

    def boarUpdate(self):
        pass


    def __str__(self):
        return self.path + '\n- ' + self.session + '\n- ' + self.repo
