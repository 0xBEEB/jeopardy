#!/usr/bin/env python

# jeopardy.py
# Hacker Jeopardy
# Copyright 2011 Thomas Schreiber <ubiquill@cat.pdx.edu>

import math, sys
import json
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import game

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
        self.gameLoader = game.GameLoader()
        self.initUI()

    def initUI(self):

        game = self.gameLoader.loadGame()
        questions = game.questions
        topics = questions.keys()


        grid = QGridLayout()

        i = 0
        for topic in topics:
            title = QLabel(topic)
            title.setFixedHeight(25)
            title.setAlignment(Qt.AlignHCenter)
            grid.addWidget(title, 0, i)
            j = 1
            for question in questions[topic]:
                button = QPushButton(str(question.value))
                button.question = question
                button.show_q = False
                self.connect(button, SIGNAL('clicked()'), self.spawnQuest)
                button.setSizePolicy(QSizePolicy.Expanding,
                                     QSizePolicy.Expanding)
                grid.addWidget(button, j, i)
                j = j + 1
            i = i + 1     

        self.player1 = QPushButton('Player 1')
        self.connect(self.player1, SIGNAL('clicked()'), self.setupPlayerOne)
        self.player1.setFlat(True)
        grid.addWidget(self.player1, 6, 0)

        self.player2 = QPushButton('Player 2')
        self.connect(self.player2, SIGNAL('clicked()'), self.setupPlayerTwo)
        self.player2.setFlat(True)
        grid.addWidget(self.player2, 6, 2)

        self.player3 = QPushButton('Player 3')
        self.connect(self.player3, SIGNAL('clicked()'), self.setupPlayerThree)
        self.player3.setFlat(True)
        grid.addWidget(self.player3, 6, 4)

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
        button = self.sender()
        if button.show_q:
            button.setText(str(button.question.value))
            button.show_q = False
        else:
            button.setText(button.question.question)
            button.show_q = True

if __name__ == "__main__":

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.showFullScreen()
    sys.exit(app.exec_())

