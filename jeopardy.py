#!/usr/bin/env python

# jeopardy.py
# Hacker Jeopardy
# Copyright 2011 Thomas Schreiber <ubiquill@cat.pdx.edu>

import math, sys
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Hacker Jeopardy')

        topics = ['topic1', 'topic2', 'topic3', 'topic4', 'topic5']

        questions = [ '100', '100', '100', '100', '100',
                      '200', '200', '200', '200', '200',
                      '300', '300', '300', '300', '300',
                      '400', '400', '400', '400', '400',
                      '500', '500', '500', '500', '500' ]

        grid = QtGui.QGridLayout()

        i = 0
        pos = [ (0,0), (0,1), (0,2), (0,3), (0,4),
                (1,0), (1,1), (1,2), (1,3), (1,4),
                (2,0), (2,1), (2,2), (2,3), (2,4),
                (3,0), (3,1), (3,2), (3,3), (3,4),
                (4,0), (4,1), (4,2), (4,3), (4,4),
                (5,0), (5,1), (5,2), (5,3), (5,4) ]

        for topic in topics:
            title = QtGui.QLabel(topic)
            title.setFixedHeight(25)
            title.setAlignment(QtCore.Qt.AlignHCenter)
            grid.addWidget(title, pos[i][0], pos[i][1])
            i = i + 1

        for question in questions:
            button = QtGui.QPushButton(question)
            button.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                 QtGui.QSizePolicy.Expanding)
            grid.addWidget(button, pos[i][0], pos[i][1])
            i = i + 1
            if (i == 5):
                i = 0

        self.setLayout(grid)


app = QtGui.QApplication(sys.argv)
mw = MainWindow()
mw.show()
sys.exit(app.exec_())

