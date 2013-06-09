# coding=utf-8

# Tool for generating content of semester works index for Software Engineering chair of St. Petersburg State University.
# See http://se.math.spbu.ru/SE/YearlyProjects/2012/list for example of output and https://www.dropbox.com/sh/ob7g6zeur45mgol/1x9riSzSXV for example of possible input.
# Usage: copy this script into a directory with semester works and run it. Output will appear in output.txt.

import os
import re

year = 2013

class Student(object):
	__template = "  <li><b>  </b>\n"  \
		"    <br />\n" \
		"%s" \
		"  </li>\n\n"

	__fileTemplate = "    <a href=\"YearlyProjects/" + "%d" % year + "/%s/%s\">%s</a>\n"
	__reportTemplate = "Отчёт"
	__presentationTemplate = "Презентация"
	__reviewTemplate = "Отзыв"

	def __init__(self, name, group):
		self.presentation = ""
		self.report = ""
		self.review = ""
		self.name = name
		self.group = group
	
	def __str__(self):
		return "Name: " + self.name + ", report: " + self.report + ", presentation: " + self.presentation + ", review: " + self.review
	
	def __repr__(self):
		return self.__str__()

	def updateDocument(self, file, documentType):
		if documentType == "presentation":
			self.presentation = file
		elif documentType == "report":	
			self.report = file
		elif documentType == "review":	
			self.review = file
	
	def generate(self):
		body = ""
		if self.report != "":
			body += self.__fileTemplate % (self.group, self.report, self.__reportTemplate)
		if self.presentation != "":
			body += self.__fileTemplate % (self.group, self.presentation, self.__presentationTemplate)
		if self.review != "":
			body += self.__fileTemplate % (self.group, self.review, self.__reviewTemplate)
		return self.__template % body

students = []

def fileInfo(fileName):
	group = ""
	match = re.search('(\d\d\d)-([A-Z]\w*)-([A-Z]\w*)-.*', fileName)
	resultNames = []
	if match:
		group = match.group(1)
		resultNames.append(match.group(2))
		resultNames.append(match.group(3))
	else:
		match = re.search('(\d\d\d)-([A-Z]\w*)-.*', fileName)
		if match:
			group = match.group(1)
			resultNames.append(match.group(2))

	resultType = "unknown"
	if "report" in fileName:
		resultType = "report"
	elif "review" in fileName:
		resultType = "review"
	elif "presentation" in fileName:
		resultType = "presentation"

	return group, resultNames, resultType

def find(predicate, list):
	for item in list:
		if predicate(item):
			return item
	return None

files = os.listdir(".")

for file in files:
	group, namesList, documentType = fileInfo(file)
	for name in namesList:
		student = find(lambda student: student.name == name, students)
		if student == None:
			student = Student(name, group)
			students.append(student)
		student.updateDocument(file, documentType)

output = open("output.txt", "w")
for student in students:
	output.write(student.generate())
output.close()	