#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from sort_photo import sort
from ui import Ui_MainWindow
from PySide.QtGui import (QApplication, QMainWindow, QTextEdit,
                         QPushButton,  QMessageBox, QFileDialog,QComboBox)


class MainWindow(Ui_MainWindow, QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow,self).__init__(parent)
		self.setupUi(self)
		self.min = 0
		self.copy = 1

		self.connect_vidgets()

	def connect_vidgets(self):
		'''define actions to vidgets and apropriate respoce'''
		self.pushButton.clicked.connect(self.get_paths)
		self.pushButton_2.clicked.connect(self.get_search_place)
		self.pushButton_4.clicked.connect(self.start)
		self.radioButton.toggled.connect(self.copy_check)
		self.comboBox.activated.connect(self.get_min_amounth) 

	def get_min_amounth(self):
		self.min = self.comboBox.currentText()

	def copy_check(self):
		if self.radioButton.isChecked():
			self.copy = 0
		else:
			self.copy = 1

	def start(self):
		if not self.min:
			pass
		else:
			app = sort(self.disc, self.seachPlace, self.min, self.copy)

	def get_paths(self):
		self.disc = QFileDialog.getExistingDirectory(self,("Open Directory"))
		self.label.setText(QApplication.translate("MainWindow", self.disc.encode('utf-8'), None, QApplication.UnicodeUTF8))

	def get_search_place(self):
		self.seachPlace = QFileDialog.getExistingDirectory(self,("Open Directory"))
		self.label_2.setText(QApplication.translate("MainWindow", self.seachPlace.encode('utf-8'), None, QApplication.UnicodeUTF8))



if __name__ == "__main__":
	app = QApplication(sys.argv)
	frame=MainWindow()
	frame.show()
	app.exec_()