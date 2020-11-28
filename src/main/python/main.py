from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets

import Design
import sys

class RandomFetching(QtWidgets.QMainWindow,Design.Ui_MainWindow):
	def __init__(self,parent=None):
		super(RandomFetching,self).__init__()
		self.setupUi(self)



if __name__ == '__main__':
	appctxt = ApplicationContext()
	page = RandomFetching()
	page.show()
	exit_code = appctxt.app.exec_()  
	sys.exit(exit_code)