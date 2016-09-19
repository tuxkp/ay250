import json, requests
import smtplib
import os
import word2number.w2n as w2n


class MontyAI():
	request = ''
	response = ''
	data = ''
	json = ''
	resp = ''
	joke_url = "http://api.icndb.com/jokes/random"
	whatami = ''
	operators = ["plus", "minus", "times", "divide"]
	def __init__(self,string):
		if self.isMontyRequest(string):
			request = string.partition(' ')[2]
			if self.isJoke(request):
				print("Joke!!!")
				self.getJoke()
			if self.isMath(request):
				print("Math!!!")
				self.doMath(request)
			if self.isEmail(request):
				print("Email!!!")
				self.doEmail(request)

	def isMontyRequest(self,string):
		name = string.partition(' ')[0]
		if name == "monty" or name == 'manti' or name == 'monte':
			return 1
		else:
			return 0
	def isJoke(self,string):
		if string == 'tell me a joke':
			self.whatami = 'joke'
			return 1
		else:
			return 0
	def getJoke(self):
		self.resp = requests.get(url=self.joke_url, params = dict())
		self.data = json.loads(self.resp.text)
		self.response = self.data['value']['joke']
	def isMath(self,string):
		if string.partition(' ')[0] == 'calculate':
			self.whatami = 'math'
			return 1
		else:
			return 0
	def doMath(self,string):
		words = string.split(' ')
		count = 1
		arg1 = 0
		word = words[count]
		while word not in self.operators:
			arg1 = arg1 + w2n.word_to_num(word)
			count = count+1
			word = words[count]
		operator = words[count]
		arg2 = 0
		for i in words[count+1:]:
			arg2 = arg2 + w2n.word_to_num(i)
		value = 0
		print(operator)
		if operator == "plus":
			value = arg1 + arg2
		if operator == "times":
			value = arg1 * arg2
		if operator == "minus":
			value = arg1 - arg2
		if operator == "divide":
			value = arg1 / arg2
		self.response = value

	def isEmail(self,string):
		if string.partition(' ')[0] == 'email':
			return 1
		else:
			return 0
	def doEmail(self,string):
		mail_server = "localhost"
		email_address = "wongmeiyen@gmail.com"
		words = iter(string.split(' '))
		subject = ""
		body = ""
		for word in words:
			if word == 'subject':
				subject = next(words)
			if word == 'body':
				body = next(words)
		msg = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}".format(email_address, email_address, subject, body)
		server = smtplib.SMTP(mail_server)
		server.set_debuglevel(1)
		server.sendmail(email_address, email_address, msg)
		server.quit()



#text_input = "monty tell me a joke"
#text_input = "monty calculate thirty one plus twenty two"
#text_input = "monty email me with subject hello and body goodbye"
#AI = MontyAI(text_input)
#print(AI.response)
