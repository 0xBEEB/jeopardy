#!/usr/bin/env python

# jeopardy.py
# Hacker Jeopardy
# Copyright 2011 Thomas Schreiber <ubiquill@cat.pdx.edu>

import math, sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class QuestWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        layout = QHBoxLayout()
        answerLabel = QLabel("The answer is")
        layout.addWidget(answerLabel)
        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("ANSWER")


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()


    def initUI(self):

        topics = ['topic1', 'topic2', 'topic3', 'topic4', 'topic5']

        questions = [ '100', '100', '100', '100', '100',
                      '200', '200', '200', '200', '200',
                      '300', '300', '300', '300', '300',
                      '400', '400', '400', '400', '400',
                      '500', '500', '500', '500', '500' ]


        grid = QGridLayout()

        i = 0
        pos = [ (0,0), (0,1), (0,2), (0,3), (0,4),
                (1,0), (1,1), (1,2), (1,3), (1,4),
                (2,0), (2,1), (2,2), (2,3), (2,4),
                (3,0), (3,1), (3,2), (3,3), (3,4),
                (4,0), (4,1), (4,2), (4,3), (4,4),
                (5,0), (5,1), (5,2), (5,3), (5,4),
                (6,0), (6,1), (6,2), (6,3), (6,4) ]

        for topic in topics:
            title = QLabel(topic)
            title.setFixedHeight(25)
            title.setAlignment(Qt.AlignHCenter)
            grid.addWidget(title, pos[i][0], pos[i][1])
            i = i + 1

        for question in questions:
            button = QPushButton(question)
            self.connect(button, SIGNAL('clicked()'), self.spawnQuest)
            button.setSizePolicy(QSizePolicy.Expanding,
                                 QSizePolicy.Expanding)
            grid.addWidget(button, pos[i][0], pos[i][1])
            i = i + 1

        self.player1 = QPushButton('Player 1')
        self.connect(self.player1, SIGNAL('clicked()'), self.setupPlayerOne)
        self.player1.setFlat(True)
        grid.addWidget(self.player1, pos[i][0], pos[i][1])
        i = i + 2

        self.player2 = QPushButton('Player 2')
        self.connect(self.player2, SIGNAL('clicked()'), self.setupPlayerTwo)
        self.player2.setFlat(True)
        grid.addWidget(self.player2, pos[i][0], pos[i][1])
        i = i + 2

        self.player3 = QPushButton('Player 3')
        self.connect(self.player3, SIGNAL('clicked()'), self.setupPlayerThree)
        self.player3.setFlat(True)
        grid.addWidget(self.player3, pos[i][0], pos[i][1])

        self.widget = QWidget()
        self.widget.setLayout(grid)

        self.setCentralWidget(self.widget)
        self.setWindowTitle('Hacker Jeopardy')


    def setupPlayerOne(self):
        text, ok = QInputDialog.getText(self, 'Player 1', 'Enter name:')
        if ok:
            self.player1.setText(str(text))

    def setupPlayerTwo(self):
        text, ok = QInputDialog.getText(self, 'Player 2', 'Enter name:')
        if ok:
            self.player2.setText(str(text))

    def setupPlayerThree(self):
        text, ok = QInputDialog.getText(self, 'Player 3', 'Enter name:')
        if ok:
            self.player3.setText(str(text))


    def spawnQuest(self):
        self.questWindow = QuestWindow()
        self.questWindow.show()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.showFullScreen()
    sys.exit(app.exec_())

