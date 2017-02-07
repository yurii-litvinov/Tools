# coding=utf-8

# Tool for generating content of diploma works index for Software Engineering chair of St. Petersburg State University.
# See http://se.math.spbu.ru/SE/YearlyProjects/2012/list for example of output and https://www.dropbox.com/sh/ob7g6zeur45mgol/1x9riSzSXV for example of possible input.
# Usage: copy this script into a directory with semester works and run it. Output will appear in output.txt.
# This script needs file 'table.csv' in the same directory (the first column must be full name of student, second column - student surname in english, fourth column - thesis theme).
# Surname in english has to be the same as surname in title of files with thesis, review, presentation etc.
# If there is no such file, output.txt will be generated, but without full name and theme lines.

import os
import re
import csv

year = 2015

class Student(object):

	__template = "    <tr class=\"%s\">\n" \
				 "%s" \
				 "    </tr>\n\n"

	__titleTemplate = "      <td> %s </td>\n"
	__emptyTitleTemplate = "      <td>  </td>\n"

	__fileTemplate = "      <td><a href=\"bmo/%s\">%s</a></td>\n"
	__reportTemplate = "Текст"
	__presentationTemplate = "Презентация"
	__sourcesTemplate = "Код"
	__advisorReviewTemplate = "Отзыв научного руководителя"
	__reviewerReviewTemplate = "Отзыв рецензента"

	def __init__(self, name, fullName, theme):
		self.presentation = ""
		self.report = ""
		self.sources = ""
		self.advisorReview = ""
		self.reviewerReview = ""
		self.name = name
		self.fullName = fullName
		self.theme = theme
	
	def __str__(self):
		return "Name: " + self.name + ", report: " + self.report + ", presentation: " \
			+ self.presentation + ", sources: " + self.sources + ", advisor review: " \
			+ self.advisorReview + ", reviewer review: " + self.reviewerReview
	
	def __repr__(self):
		return self.__str__()

	def updateDocument(self, file, documentType):
		if documentType == "presentation":
			self.presentation = file
		elif documentType == "report":	
			self.report = file
		elif documentType == "sources":	
			self.sources = file
		elif documentType == "advisorReview":	
			self.advisorReview = file
		elif documentType == "reviewerReview":	
			self.reviewerReview = file
	
	def generate(self, docClass):
		documentClass = "odd"
		if docClass == 0:
			documentClass = "even"	
		body = ""

		if self.fullName != "":
			body += self.__titleTemplate % (self.fullName)
		else:
			body += self.__emptyTitleTemplate

		if self.theme != "":
			body += self.__titleTemplate % (self.theme)
		else:
			body += self.__emptyTitleTemplate

		if self.report != "":
			body += self.__fileTemplate % (self.report, self.__reportTemplate)
		else:
			body += "      <td>текст не представлен</td>\n"

		if self.presentation != "":
			body += self.__fileTemplate % (self.presentation, self.__presentationTemplate)
		else:
			body += "      <td>презентация не представлена</td>\n"

		if self.advisorReview != "":
			body += self.__fileTemplate % (self.advisorReview, self.__advisorReviewTemplate)
		else:
			body += "      <td>отзыв научного руководителя не представлен</td>\n"

		if self.reviewerReview != "":
			body += self.__fileTemplate % (self.reviewerReview, self.__reviewerReviewTemplate)
		else:
			body += "      <td>отзыв рецензента не представлен</td>\n"

		if self.sources != "":
			body += self.__fileTemplate % (self.sources, self.__sourcesTemplate)
		else:
			body += "      <td>код не представлен</td>\n"

		return self.__template % (documentClass, body)

students = []

def fileInfo(fileName):
	group = ""
	match = re.search('444-([A-Z]\w*)-([a-z]\w*).*', fileName)
	resultName = ""
	if match:
		resultName = match.group(1)

	resultType = "unknown"
	if "report" in fileName:
		resultType = "report"
	elif "presentation" in fileName:
		resultType = "presentation"
	elif "Sources" in fileName:
		resultType = "sources"
	elif "advisor-review" in fileName:
		resultType = "advisorReview"	
	elif "reviewer-review" in fileName:
		resultType = "reviewerReview"
	return resultName, resultType

def find(predicate, list):
	for item in list:
		if predicate(item):
			return item
	return None


def addValueToDictionary(d, key, value):
	if key not in d and key:
		d[key] = value


def getValueFromDictionary(d, key):
	value = ""
	if key in d:
		value = d[key]

	return value


def initDictionaries(csvFile):
	fullNames = {}
	themes = {}
	with open(csvFile, 'rt', encoding='utf-8') as file:
		csvReader = csv.reader(file)
		for row in csvReader:
			key = row[1]
			fullName = row[0]
			theme = row[3]

			addValueToDictionary(fullNames, key, fullName)
			addValueToDictionary(themes, key, theme)
	return fullNames, themes


files = os.listdir(".")

fullNames, themes = {}, {}
tableName = 'table.csv'

if os.path.isfile(tableName):
	fullNames, themes = initDictionaries(tableName)

for file in files:
	name, documentType = fileInfo(file)
	student = find(lambda student: student.name == name, students)
	if student == None:
		fullName = getValueFromDictionary(fullNames, name)
		theme = getValueFromDictionary(themes, name)

		student = Student(name, fullName, theme)
		students.append(student)
	student.updateDocument(file, documentType)

output = open("output.txt", "w")
i = 1
for student in students:
	output.write(student.generate(i % 2))
	i = i + 1
output.close()	