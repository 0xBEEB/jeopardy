import json
import os
import random

class Question(object):
	def __init__(self, question, value, isDD=False):
		self.question = question
		self.value = value
		self.isDD = isDD

class Game(object):
	def __init__(self, questions, stage):
		self.questions = {}
		self.stage = stage
		for key, value in questions.items():
			qs = []
			self.questions[key] = qs
			i = 1
			for q in value:
				qs.append(Question(q, i*100*self.stage))
				i = i + 1

class GameLoader(object):
	def __init__(self, stage, gamesdir='data/games'):
		self.gamesdir = gamesdir
		self.stage = stage

	def loadGame(self, name=None):
		if name == None:
			options = os.listdir(self.gamesdir)
			name = options[int(random.random() * len(options))]
		questions_fd = open(self.gamesdir + '/' + name)
		questions = json.load(questions_fd)

		return Game(questions, self.stage)

if __name__ == '__main__':
	loader = GameLoader()
	game = loader.loadGame()
	print game.questions

