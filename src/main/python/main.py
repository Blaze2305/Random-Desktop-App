from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets
from requests import get
import Design
import sys
from random import choice

class RandomFetching(QtWidgets.QMainWindow,Design.Ui_MainWindow):
	def __init__(self,parent=None):
		super(RandomFetching,self).__init__()
		self.setupUi(self)
		self.InsultMeButton.clicked.connect(self.fetchInsult)
		self.preloadInsults()

	def fetchInsult(self):
		self.InsultTextBox.clear()
		category = self.getCheckedRadioButton()
		if category:
			print(f"FETCHING INSULT FOR CATEGORY {category}")
			insult = choice(self.insults[category])
			self.InsultTextBox.append(insult)
		else:
			self.InsultTextBox.apped("NO INSULT TYPE SELECTED")

	def getCheckedRadioButton(self):
		if self.ShakespeareButton.isChecked():
			return "shakespeare"
		if self.AyeButton.isChecked():
			return "pirate"
		if self.ScotButton.isChecked():
			return "scottish"
		if self.SciFiButton.isChecked():
			return "scifi"
		if self.YeOldButton.isChecked():
			return "medieval"
		return None

	def preloadInsults(self):
		insultsFiles = ["pirate","scifi","scottish","medieval","shakespeare"]
		insults = {}
		for file in insultsFiles:
			insultsFilePath = ApplicationContext().get_resource(f"{file}.txt")
			with open(insultsFilePath) as insultsFile:
				insultsList = insultsFile.read().split("\n")
				insults[file] = insultsList
		self.insults = insults


if __name__ == '__main__':
	appctxt = ApplicationContext()
	page = RandomFetching()
	page.show()
	exit_code = appctxt.app.exec_()  
	sys.exit(exit_code)