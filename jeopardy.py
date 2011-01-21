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
import buzzer

class FinalJeopardy(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        final = self.gameLoader.loadGame()
        questions = final.questions
        topics = questions.keys()

        topic = topics[0]
        self.question = questions[topic][0]

        layout = QGridLayout()

        self.revealButton = QPushButton(">")
        self.connect(self.revealButton, SIGNAL('clicked()'), self.revealQuestion)
        layout.addWidget(self.revealButton, 0, 0, 4, 1)


        self.questionLabel = QLabel(topic)
        layout.addWidget(self.questionLabel, 0, 1, 4, 5)

        self.player1 = QPushButton('Player1')
        self.connect(self.player1, SIGNAL('clicked()'), self.player1Answer)
        layout.addWidget(self.player1, 5, 0, 1, 1) 

        self.player2 = QPushButton('Player2')
        self.connect(self.player2, SIGNAL('clicked()'), self.player2Answer)
        layout.addWidget(self.player2, 5, 2, 1, 1)

        self.player3 = QPushButton('Player3')
        self.connect(self.player3, SIGNAL('clicked()'), self.player3Answer)
        layout.addWidget(self.player3, 5, 4, 1, 1)

        self.player1ScoreLabel = QTextEdit('0')
        self.player1ScoreLabel.setMaximumHeight(40)
        layout.addWidget(self.player1ScoreLabel, 6, 0, 1, 1)
        self.player2ScoreLabel = QTextEdit('0')
        self.player2ScoreLabel.setMaximumHeight(40)
        layout.addWidget(self.player2ScoreLabel, 6, 2, 1, 1)
        self.player3ScoreLabel = QTextEdit('0')
        self.player3ScoreLabel.setMaximumHeight(40)
        layout.addWidget(self.player3ScoreLabel, 6, 4, 1, 1)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)
        self.setWindowTitle('Final Jeopardy')

    def revealQuestion(self):
        self.questionLabel.setText(self.question.question)

    def player1Answer(self):
        text, ok = QInputDialog.getText(self, self.player1.text(), 'Bet:')
        if ok:
            self.player1Score += int(text)
        self.player1ScoreLabel.setText(str(self.player1Score))

    def player2Answer(self):
        text, ok = QInputDialog.getText(self, self.player2.text(), 'Bet:')
        if ok:
            self.player2Score += int(text)
        self.player2ScoreLabel.setText(str(self.player2Score))

    def player3Answer(self):
        text, ok = QInputDialog.getText(self, self.player3.text(), 'Bet:')
        if ok:
            self.player3Score += int(text)
        self.player3ScoreLabel.setText(str(self.player3Score))


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
        if self.sender() == self.winButton:
            mw.showBoard()
        else:
            timer = QTimer(self)
            timer.timeout.connect(mw.waitForBuzzer)
            timer.setSingleShot(True)
            timer.start(100)
        mw.buzzState = True
        self.close()


class MainWindow(QMainWindow):
    def __init__(self, stage):
        self.buzzerHandlers = {
            1: self.buzzInOne,
            2: self.buzzInTwo,
            3: self.buzzInThree,
        }

        self.buzzerMan = buzzer.BuzzerManager('/dev/ttyACM0')
        self.gameLoader = game.GameLoader(1, 'data/games/fjeopardy')
        QMainWindow.__init__(self)
        self.stage = stage
        self.buzzState = True
        if stage == 1:
            self.gameLoader = game.GameLoader(1, 'data/games/jeopardy')
        if stage == 2:
            self.gameLoader = game.GameLoader(2, 'data/games/djeopardy')
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

        self.dailyDouble = (random.randrange(5), random.randrange(5)+1)
        self.dailyDouble2 = (100, 100)
        if self.stage == 2:
            self.dailyDouble2 = (random.randrange(5), random.randrange(5)+1)
            while self.dailyDouble == self.dailyDouble2:
                self.dailyDouble2 = (random.randrange(5), random.randrange(5)+1)


        self.mainLayout = QStackedLayout()
        self.boardBox = QWidget()
        self.questionBox = QWidget()
        grid = QGridLayout()
        self.mainLayout.addWidget(self.boardBox)
        self.mainLayout.addWidget(self.questionBox)
        self.mainLayout.setCurrentWidget(self.boardBox)

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
                if (  (j == self.dailyDouble[1]  and  i == self.dailyDouble[0]) 
                   or (j == self.dailyDouble2[1] and  i == self.dailyDouble2[0])):
                    button.question.isDD = True
                self.connect(button, SIGNAL('clicked()'), self.spawnQuest)
                button.setSizePolicy(QSizePolicy.Expanding,
                                             QSizePolicy.Expanding)
                grid.addWidget(button, j, i)
                j = j + 1
            i = i + 1     

        # This is the question layout that appears when a question is chosen
        questionLayout = QVBoxLayout()
        self.bigQuestionLabel = QLabel('No Question')
        returnButton = QPushButton('<')
        self.connect(returnButton, SIGNAL('clicked()'), self.showBoard)
        questionLayout.addWidget(self.bigQuestionLabel)
        questionLayout.addWidget(returnButton)
        self.questionBox.setLayout(questionLayout)

        self.player1 = QPushButton('Player 1')
        self.connect(self.player1, SIGNAL('clicked()'), self.setupPlayerOne)
        self.player1.setFlat(True)
        grid.addWidget(self.player1, 6, 0)

        self.player1Buzz = QPushButton('BZZZ!')
        self.connect(self.player1Buzz, SIGNAL('clicked()'), self.buzzInOne)
        grid.addWidget(self.player1Buzz, 7, 0)

        self.player1ScoreLabel = QPushButton(str(self.player1Score))
        self.player1ScoreLabel.setFlat(True)
        self.player1ScoreLabel.setMaximumHeight(40)
        grid.addWidget(self.player1ScoreLabel, 8, 0)

        self.player2 = QPushButton('Player 2')
        self.connect(self.player2, SIGNAL('clicked()'), self.setupPlayerTwo)
        self.player2.setFlat(True)
        grid.addWidget(self.player2, 6, 2)

        self.player2Buzz = QPushButton('BZZZ!')
        self.connect(self.player2Buzz, SIGNAL('clicked()'), self.buzzInTwo)
        grid.addWidget(self.player2Buzz, 7, 2)

        self.player2ScoreLabel = QPushButton(str(self.player2Score))
        self.player2ScoreLabel.setFlat(True)
        self.player2ScoreLabel.setMaximumHeight(40)
        grid.addWidget(self.player2ScoreLabel, 8, 2)

        self.player3 = QPushButton('Player 3')
        self.connect(self.player3, SIGNAL('clicked()'), self.setupPlayerThree)
        self.player3.setFlat(True)
        grid.addWidget(self.player3, 6, 4)

        self.player3Buzz = QPushButton('BZZZ!')
        self.connect(self.player3Buzz, SIGNAL('clicked()'), self.buzzInThree)
        grid.addWidget(self.player3Buzz, 7, 4)

        self.player3ScoreLabel = QPushButton(str(self.player3Score))
        self.player3ScoreLabel.setFlat(True)
        self.player3ScoreLabel.setMaximumHeight(40)
        grid.addWidget(self.player3ScoreLabel, 8, 4)

        self.randButton = QPushButton('Pseudo Random')
        self.connect(self.randButton, SIGNAL('clicked()'), self.pickRand)
        grid.addWidget(self.randButton, 9, 1)

        self.nextButton = QPushButton('Next Round')
        self.connect(self.nextButton, SIGNAL('clicked()'), self.nextRound)
        grid.addWidget(self.nextButton, 9, 3)

        self.widget = QWidget()
        self.boardBox.setLayout(grid)
        self.widget.setLayout(self.mainLayout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle('Hacker Jeopardy')


    def showBoard(self):
        self.mainLayout.setCurrentWidget(self.boardBox)

    def setupPlayerOne(self):
        text, ok = QInputDialog.getText(self, 'Player 1', 'Enter name:')
        if ok:
            self.player1.setText(str(text))

    def buzzInOne(self):
        if self.buzzState == True:
            self.buzzState = False
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
        if self.buzzState == True:
            self.buzzState = False
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
        if self.buzzState == True:
            self.buzzState = False
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

    def pickRand(self):
        random.seed()
        randPlayerNum = random.randrange(3)
        if randPlayerNum == 0:
            randPlayer = self.player1.text()
        if randPlayerNum == 1:
            randPlayer = self.player2.text()
        if randPlayerNum == 2:
            randPlayer = self.player3.text()
        ok = QMessageBox.question(self, 'I pick ...', randPlayer, QMessageBox.Ok)

    def nextRound(self):        
        if self.stage == 1:
            self.stage += 1
            self.mw2 = MainWindow(self.stage)
            self.mw2.player1.setText(self.player1.text())
            self.mw2.player2.setText(self.player2.text())
            self.mw2.player3.setText(self.player3.text())
            self.mw2.player1Score = self.player1Score
            self.mw2.player1ScoreLabel.setText(str(self.mw2.player1Score))
            self.mw2.player2Score = self.player2Score
            self.mw2.player2ScoreLabel.setText(str(self.mw2.player2Score))
            self.mw2.player3Score = self.player3Score
            self.mw2.player3ScoreLabel.setText(str(self.mw2.player3Score))
            self.mw2.showFullScreen()
            self.hide()
        elif self.stage == 2:
            self.stage += 1
            self.fw = FinalJeopardy()
            self.fw.player1.setText(self.player1.text())
            self.fw.player2.setText(self.player2.text())
            self.fw.player3.setText(self.player3.text())
            self.fw.player1Score = self.player1Score
            self.fw.player1ScoreLabel.setText(str(self.fw.player1Score))
            self.fw.player2Score = self.player2Score
            self.fw.player2ScoreLabel.setText(str(self.fw.player2Score))
            self.fw.player3Score = self.player3Score
            self.fw.player3ScoreLabel.setText(str(self.fw.player3Score))
            self.fw.show()
            self.hide()
        
    def waitForBuzzer(self):
        try:
            resp = self.buzzerMan.getBuzzer()
            self.buzzerHandlers[resp]()
        except KeyError:
            print 'invalid response'

    def spawnQuest(self):

        button = self.sender()
        self.bigQuestionLabel.setText(button.question.question)
        if button.question.isDD == True:
            text, ok = QInputDialog.getText(self, 'DAILY DOUBLE', 'DAILY DOUBLE')
            if ok:
                button.question.value = int(text)
        if button.show_q:
            button.setText(str(button.question.value))
            button.show_q = False
        else:
            self.mainLayout.setCurrentWidget(self.questionBox)
            button.show_q = True
            button.setFlat(True)
            self.currValue = button.question.value
            self.currQuestion = button.question.question
		
        self.buzzerMan.s.flushInput()
        timer = QTimer(self)
        timer.timeout.connect(self.waitForBuzzer)
        timer.setSingleShot(True)
        timer.start(100)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    random.seed()
    stage = 1
    mw = MainWindow(stage)
    mw.showFullScreen()
    sys.exit(app.exec_())

