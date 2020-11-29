from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets,QtGui,QtCore
from requests import post,get
import Design
import sys
from os import environ
from random import choice


DEEP_AI_API_KEY = environ['DEEP_AI_API_KEY']

class RandomFetching(QtWidgets.QMainWindow,Design.Ui_MainWindow):
	def __init__(self,parent=None):
		super(RandomFetching,self).__init__()
		self.setupUi(self)
		self.InsultMeButton.clicked.connect(self.fetchInsult)
		self.ImageSearchButton.clicked.connect(self.fetchImage)
		self.InsultTextBox.setFont(QtGui.QFont("Roboto",25))
		self.label_3.setOpenExternalLinks(True)
		self.label_2.setOpenExternalLinks(True)
		self.preloadInsults()


	def fetchImage(self):
		seedText = self.ImageSearchBox.toPlainText()
		if not seedText:
			self.AlertError("Seed Text is empty")
			return

		data = post(
			"https://api.deepai.org/api/text2img",
			data={
				'text': seedText,
			},
			headers={'api-key': DEEP_AI_API_KEY}
		)
		print(data.status_code)
		if data.status_code == 200:
			data = data.json()
		else:
			self.AlertError("Unable to fetch the generated image")
			return
		
		url = data['output_url']

		imageData = get(url).content

		image = QtGui.QImage()
		image.loadFromData(imageData)

		pixelImage = QtGui.QPixmap(image)
		self.ImageView.setPixmap(pixelImage)


	def fetchInsult(self):
		self.InsultTextBox.clear()
		category = self.getCheckedRadioButton()
		if category:
			print(f"FETCHING INSULT FOR CATEGORY {category}")
			insult = choice(self.insults[category])
			self.InsultTextBox.append(insult)
		else:
			self.InsultTextBox.append("NO INSULT TYPE SELECTED")

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

	def AlertError(self,message):
		alertBox = QtWidgets.QMessageBox()
		alertBox.setText(message)
		alertBox.exec_()


if __name__ == '__main__':
	appctxt = ApplicationContext()
	page = RandomFetching()
	page.show()
	exit_code = appctxt.app.exec_()  
	sys.exit(exit_code)