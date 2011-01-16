import json

topics = {}
for i in range(5):
	questions = []
	for j in range(5):
		questions.append('Question %i' % j)
	topics['Topic %i' % i] = questions

print json.dumps(topics)

