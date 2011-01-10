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

    def spawnQuest(self):
        Answer = QtGui.QMessageBox.question(self, 'Answer', 'The mascot of Linux.',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, 
                                            QtGui.QMessageBox.No)


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
                (5,0), (5,1), (5,2), (5,3), (5,4),
                (6,0), (6,1), (6,2), (6,3), (6,4) ]

        for topic in topics:
            title = QtGui.QLabel(topic)
            title.setFixedHeight(25)
            title.setAlignment(QtCore.Qt.AlignHCenter)
            grid.addWidget(title, pos[i][0], pos[i][1])
            i = i + 1

        for question in questions:
            button = QtGui.QPushButton(question)
            self.connect(button, QtCore.SIGNAL('clicked()'), self.spawnQuest)
            button.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                 QtGui.QSizePolicy.Expanding)
            grid.addWidget(button, pos[i][0], pos[i][1])
            i = i + 1

        self.player1 = QtGui.QPushButton('Player 1')
        self.connect(self.player1, QtCore.SIGNAL('clicked()'), self.setupPlayerOne)
        self.player1.setFlat(True)
        grid.addWidget(self.player1, pos[i][0], pos[i][1])
        i = i + 2

        self.player2 = QtGui.QPushButton('Player 2')
        self.connect(self.player2, QtCore.SIGNAL('clicked()'), self.setupPlayerTwo)
        self.player2.setFlat(True)
        grid.addWidget(self.player2, pos[i][0], pos[i][1])
        i = i + 2

        self.player3 = QtGui.QPushButton('Player 3')
        self.connect(self.player3, QtCore.SIGNAL('clicked()'), self.setupPlayerThree)
        self.player3.setFlat(True)
        grid.addWidget(self.player3, pos[i][0], pos[i][1])

        self.setLayout(grid)


    def setupPlayerOne(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Player 1', 'Enter name:')
        if ok:
            self.player1.setText(str(text))

    def setupPlayerTwo(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Player 2', 'Enter name:')
        if ok:
            self.player2.setText(str(text))

    def setupPlayerThree(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Player 3', 'Enter name:')
        if ok:
            self.player3.setText(str(text))

app = QtGui.QApplication(sys.argv)
mw = MainWindow()
mw.show()
sys.exit(app.exec_())

