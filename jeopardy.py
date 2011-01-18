#!/usr/bin/env python

# jeopardy.py
# Hacker Jeopardy
# Copyright 2011 Thomas Schreiber <ubiquill@cat.pdx.edu>

import sys
import random
import json
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import game

class BuzzAlert(QMainWindow):
    def __init__(self, player, value, question):
        QMainWindow.__init__(self)
	self.value = value
        layout = QGridLayout()
        self.playerLabel = QLabel(player)
        layout.addWidget(self.playerLabel, 0, 3)


        self.questionLabel = QLabel(question)
        layout.addWidget(self.questionLabel, 1, 3)

        self.valueEdit = QTextEdit(str(value))
        self.valueEdit.setMaximumHeight(30)
        layout.addWidget(self.valueEdit, 2, 3)

	self.connect(self.valueEdit, SIGNAL('textChanged()'), self.updateScore)

        self.failButton = QPushButton("FAIL")
	self.connect(self.failButton, SIGNAL('clicked()'), self.closeWin)

        self.winButton  = QPushButton("WIN")
	self.connect(self.winButton, SIGNAL('clicked()'), self.closeWin)

        layout.addWidget(self.failButton, 3, 2)
        layout.addWidget(self.winButton, 3, 4)

        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("BZZZZZ!")

    def updateScore(self):
	self.value = int(self.valueEdit.toPlainText())

    def closeWin(self):
	mw.currValue = self.value
	self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.gameLoader = game.GameLoader()
        self.initUI()

    def initUI(self):

        game = self.gameLoader.loadGame()
        questions = game.questions
        topics = questions.keys()

        self.player1Score = 0
        self.player2Score = 0
        self.player3Score = 0

        self.currValue = 0
        self.currQuestion = ""

	self.dailyDouble = (random.randrange(5), random.randrange(5) + 1)


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
		if (j == self.dailyDouble[1] and i == self.dailyDouble[0]):
		    self.connect(button, SIGNAL('clicked()'), self.ddWager)
		else:
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

        self.player1Buzz = QPushButton('BZZZ!')
        self.connect(self.player1Buzz, SIGNAL('clicked()'), self.buzzInOne)
        grid.addWidget(self.player1Buzz, 7, 0)

        self.player1ScoreLabel = QTextEdit(str(self.player1Score))
        self.player1ScoreLabel.setMaximumHeight(30)
        grid.addWidget(self.player1ScoreLabel, 8, 0)

        self.player2 = QPushButton('Player 2')
        self.connect(self.player2, SIGNAL('clicked()'), self.setupPlayerTwo)
        self.player2.setFlat(True)
        grid.addWidget(self.player2, 6, 2)

        self.player2Buzz = QPushButton('BZZZ!')
        self.connect(self.player2Buzz, SIGNAL('clicked()'), self.buzzInTwo)
        grid.addWidget(self.player2Buzz, 7, 2)

        self.player2ScoreLabel = QTextEdit(str(self.player2Score))
        self.player2ScoreLabel.setMaximumHeight(30)
        grid.addWidget(self.player2ScoreLabel, 8, 2)

        self.player3 = QPushButton('Player 3')
        self.connect(self.player3, SIGNAL('clicked()'), self.setupPlayerThree)
        self.player3.setFlat(True)
        grid.addWidget(self.player3, 6, 4)

        self.player3Buzz = QPushButton('BZZZ!')
        self.connect(self.player3Buzz, SIGNAL('clicked()'), self.buzzInThree)
        grid.addWidget(self.player3Buzz, 7, 4)

        self.player3ScoreLabel = QTextEdit(str(self.player3Score))
        self.player3ScoreLabel.setMaximumHeight(30)
        grid.addWidget(self.player3ScoreLabel, 8, 4)

        self.widget = QWidget()
        self.widget.setLayout(grid)

        self.setCentralWidget(self.widget)
        self.setWindowTitle('Hacker Jeopardy')


    def ddWager(self):
	button = self.sender()
	text, ok = QInputDialog.getText(self, 'DAILY DOUBLE', 'DAILY DOUBLE')
	if ok:
	    button.question.value = int(text)
            if button.show_q:
                button.setText(str(button.question.value))
                button.show_q = False
            else:
                button.setText(button.question.question)
                button.show_q = True
                self.currValue = button.question.value
                self.currQuestion = button.question.question



    def setupPlayerOne(self):
        text, ok = QInputDialog.getText(self, 'Player 1', 'Enter name:')
        if ok:
            self.player1.setText(str(text))

    def buzzInOne(self):
        self.buzzWin = BuzzAlert(self.player1.text(), 
				 self.currValue, 
				 self.currQuestion)
	self.connect(self.buzzWin.failButton, SIGNAL('clicked()'), self.scoreDown1)
	self.connect(self.buzzWin.winButton, SIGNAL('clicked()'), self.scoreUp1)
        self.buzzWin.show()

    def setupPlayerTwo(self):
        text, ok = QInputDialog.getText(self, 'Player 2', 'Enter name:')
        if ok:
            self.player2.setText(str(text))

    def buzzInTwo(self):
        self.buzzWin = BuzzAlert(self.player2.text(), 
				 self.currValue, 
				 self.currQuestion)
	self.connect(self.buzzWin.failButton, SIGNAL('clicked()'), self.scoreDown2)
	self.connect(self.buzzWin.winButton, SIGNAL('clicked()'), self.scoreUp2)
        self.buzzWin.show()

    def setupPlayerThree(self):
        text, ok = QInputDialog.getText(self, 'Player 3', 'Enter name:')
        if ok:
            self.player3.setText(str(text))

    def buzzInThree(self):
        self.buzzWin = BuzzAlert(self.player3.text(), 
				 self.currValue, 
				 self.currQuestion)
	self.connect(self.buzzWin.failButton, SIGNAL('clicked()'), self.scoreDown3)
	self.connect(self.buzzWin.winButton, SIGNAL('clicked()'), self.scoreUp3)
        self.buzzWin.show()

    def scoreDown1(self):
        self.player1Score -= self.currValue
	print self.player1Score
	self.player1ScoreLabel.setText(str(self.player1Score))

    def scoreDown2(self):
        self.player2Score -= self.currValue
	self.player2ScoreLabel.setText(str(self.player2Score))

    def scoreDown3(self):
        self.player3Score -= self.currValue
	self.player3ScoreLabel.setText(str(self.player3Score))

    def scoreUp1(self):
        self.player1Score += self.currValue
	self.player1ScoreLabel.setText(str(self.player1Score))

    def scoreUp2(self):
        self.player2Score += self.currValue
	self.player2ScoreLabel.setText(str(self.player2Score))

    def scoreUp3(self):
        self.player3Score += self.currValue
	self.player3ScoreLabel.setText(str(self.player3Score))


    def spawnQuest(self):
        button = self.sender()
        if button.show_q:
            button.setText(str(button.question.value))
            button.show_q = False
        else:
            button.setText(button.question.question)
            button.show_q = True
            self.currValue = button.question.value
            self.currQuestion = button.question.question

if __name__ == "__main__":

    app = QApplication(sys.argv)
    random.seed()
    mw = MainWindow()
    mw.showFullScreen()
    sys.exit(app.exec_())

