#!/usr/bin/env python3

from PyQt4 import QtGui, QtCore, uic
import serial
import time
from sys import stdout
import pyqtgraph
from PyQt4.Qt import *
import csv
import datetime
import os
import subprocess

#to re-implement dynamic progress bars
#must make change in UI file and in control file for debian packaging
#import MQProgressBar as MQProgressBar

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		# initializes MainWindow
		# connects button clicks/changes in UI to functions

		QtGui.QWidget.__init__(self)
		#uic.loadUi("teensy_gui.ui", self) # QT Developer file

		# load UI file to execute from bash script (linux-specific)
		path = os.path.dirname(os.path.abspath(__file__))
		uic.loadUi((os.path.join(path, "teensy_gui.ui")), self)

		self.setWindowTitle("i.MX WattsApp Power Profiler")

		self.graphicsView.plotItem.showGrid(True, False, 0.7)
		self.graphicsView.clear()

		### New Data tab ###

		self.tabWidget.currentChanged.connect(self.tab_changed)
		self.tabWidget.setCurrentIndex(0)

		self.minusButton.clicked.connect(self.minus_clicked)
		self.minButton.clicked.connect(self.min_clicked)
		self.maxButton.clicked.connect(self.max_clicked)
		self.plusButton.clicked.connect(self.plus_clicked)
		self.updateRateLineEdit.clear()
		self.updateRateLineEdit.setReadOnly(True)

		# set check all check boxes to unchecked
		self.checkAllCheckBox1.setChecked(False)
		self.checkAllCheckBox1.stateChanged.connect(self.check_all_changed)
		self.checkAllCheckBox2.setChecked(False)
		self.checkAllCheckBox2.stateChanged.connect(self.check_all_changed)
		self.checkAllCheckBox3.setChecked(False)
		self.checkAllCheckBox3.stateChanged.connect(self.check_all_changed)
		self.checkAllCheckBox4.setChecked(False)
		self.checkAllCheckBox4.stateChanged.connect(self.check_all_changed)

		self.stackedWidget.setCurrentIndex(0)
		self.stackedWidget.show()

		self.plainTextEdit.setReadOnly(True)
		# sets maximum number of lines held in plainTextEdit to 100 - fixed graph lag problem
		self.plainTextEdit.setMaximumBlockCount(100)
		self.lineEdit.setReadOnly(True)

		self.displayButton.clicked.connect(self.display_button_clicked)
		self.graphButton.clicked.connect(self.graph_button_clicked)

		self.serialComboBox.currentIndexChanged.connect(self.serial_combo_changed)
		self.getPortButton.clicked.connect(self.get_ports)
		self.getPortButton.click()

		self.comboBox.currentIndexChanged.connect(self.combo_changed)
		self.comboBox.lineEdit().setReadOnly(True)
		self.comboBox.lineEdit().setAlignment(QtCore.Qt.AlignCenter)

		# only show graphicsView - not plainTextEdit (index 1)
		self.stackedWidget_2.setCurrentIndex(0)

		self.displayButton.hide()
		self.graphButton.hide()
	
		self.chooseFile.hide()
		self.lineEdit.hide()
		self.startSavingStopping.hide()
		self.appendRewriteBox.hide()
		self.appendRewriteBox.setChecked(True)
			
		self.chooseFile.clicked.connect(self.choose_file_to_write)
		self.startSavingStopping.clicked.connect(self.start_or_stop_saving_data)

		self.loadConfig.clicked.connect(self.load_config)

		self.check1_1.stateChanged.connect(self.check_box_changed)
		self.check1_2.stateChanged.connect(self.check_box_changed)
		self.check1_3.stateChanged.connect(self.check_box_changed)
		self.check1_4.stateChanged.connect(self.check_box_changed)
		self.check1_5.stateChanged.connect(self.check_box_changed)
		self.check1_6.stateChanged.connect(self.check_box_changed)
		self.check1_7.stateChanged.connect(self.check_box_changed)
		self.check1_8.stateChanged.connect(self.check_box_changed)
		self.check1_9.stateChanged.connect(self.check_box_changed)
		self.check1_10.stateChanged.connect(self.check_box_changed)
		self.check2_1.stateChanged.connect(self.check_box_changed)
		self.check2_2.stateChanged.connect(self.check_box_changed)
		self.check2_3.stateChanged.connect(self.check_box_changed)
		self.check2_4.stateChanged.connect(self.check_box_changed)
		self.check2_5.stateChanged.connect(self.check_box_changed)
		self.check2_6.stateChanged.connect(self.check_box_changed)
		self.check2_7.stateChanged.connect(self.check_box_changed)
		self.check2_8.stateChanged.connect(self.check_box_changed)
		self.check2_9.stateChanged.connect(self.check_box_changed)
		self.check3_1.stateChanged.connect(self.check_box_changed)
		self.check3_2.stateChanged.connect(self.check_box_changed)
		self.check3_3.stateChanged.connect(self.check_box_changed)
		self.check3_4.stateChanged.connect(self.check_box_changed)
		self.check3_5.stateChanged.connect(self.check_box_changed)
		self.check3_6.stateChanged.connect(self.check_box_changed)
		self.check4_1.stateChanged.connect(self.check_box_changed)
		self.check4_2.stateChanged.connect(self.check_box_changed)
		self.check4_3.stateChanged.connect(self.check_box_changed)
		self.check4_4.stateChanged.connect(self.check_box_changed)
		self.check4_5.stateChanged.connect(self.check_box_changed)
		self.check4_6.stateChanged.connect(self.check_box_changed)
		self.check4_7.stateChanged.connect(self.check_box_changed)
		self.check4_8.stateChanged.connect(self.check_box_changed)

		# creates colored boxes that correspond to graph colors - New Data tab
		self.colorBox1_1.setStyleSheet("background: red")
		self.colorBox1_2.setStyleSheet("background: rgb(0,255,0)")
		self.colorBox1_3.setStyleSheet("background: blue")
		self.colorBox1_4.setStyleSheet("background: cyan")
		self.colorBox1_5.setStyleSheet("background: magenta")
		self.colorBox1_6.setStyleSheet("background: yellow")
		self.colorBox1_7.setStyleSheet("background: rgb(0,128,0)")
		self.colorBox1_8.setStyleSheet("background: rgb(255, 127, 80)")
		self.colorBox1_9.setStyleSheet("background: rgb(148, 0, 211)")
		self.colorBox1_10.setStyleSheet("background: rgb(165, 42, 42)")
		self.colorBox2_1.setStyleSheet("background: red")
		self.colorBox2_2.setStyleSheet("background: rgb(0,255,0)")
		self.colorBox2_3.setStyleSheet("background: blue")
		self.colorBox2_4.setStyleSheet("background: cyan")
		self.colorBox2_5.setStyleSheet("background: magenta")
		self.colorBox2_6.setStyleSheet("background: yellow")
		self.colorBox2_7.setStyleSheet("background: rgb(0,128,0)")
		self.colorBox2_8.setStyleSheet("background: rgb(255, 127, 80)")
		self.colorBox2_9.setStyleSheet("background: rgb(148, 0, 211)")
		self.colorBox3_1.setStyleSheet("background: red")
		self.colorBox3_2.setStyleSheet("background: rgb(0,255,0)")
		self.colorBox3_3.setStyleSheet("background: blue")
		self.colorBox3_4.setStyleSheet("background: cyan")
		self.colorBox3_5.setStyleSheet("background: magenta")
		self.colorBox3_6.setStyleSheet("background: yellow")
		self.colorBox4_1.setStyleSheet("background: red")
		self.colorBox4_2.setStyleSheet("background: rgb(0,255,0)")
		self.colorBox4_3.setStyleSheet("background: blue")
		self.colorBox4_4.setStyleSheet("background: cyan")
		self.colorBox4_5.setStyleSheet("background: magenta")
		self.colorBox4_6.setStyleSheet("background: yellow")
		self.colorBox4_7.setStyleSheet("background: rgb(0,128,0)")
		self.colorBox4_8.setStyleSheet("background: rgb(255, 127, 80)")

		### Saved Data tab ###

		self.plainTextEdit_2.setReadOnly(True)
		self.plainTextEdit_2.clear()

		self.stackedWidget_3.show()
		self.stackedWidget_3.setCurrentIndex(0)

		self.chooseSavedFile.clicked.connect(self.choose_saved_file)

		# creates colored boxes that correspond to graph colors - Saved Data tab
		self.colorBox1_11.setStyleSheet("background: red")
		self.colorBox1_12.setStyleSheet("background: rgb(0,255,0)")
		self.colorBox1_13.setStyleSheet("background: blue")
		self.colorBox1_14.setStyleSheet("background: cyan")
		self.colorBox1_15.setStyleSheet("background: magenta")
		self.colorBox1_16.setStyleSheet("background: yellow")
		self.colorBox1_17.setStyleSheet("background: rgb(0,128,0)")
		self.colorBox1_18.setStyleSheet("background: rgb(255, 127, 80)")
		self.colorBox1_19.setStyleSheet("background: rgb(148, 0, 211)")
		self.colorBox1_20.setStyleSheet("background: rgb(165, 42, 42)")
		self.colorBox2_10.setStyleSheet("background: red")
		self.colorBox2_11.setStyleSheet("background: rgb(0,255,0)")
		self.colorBox2_12.setStyleSheet("background: blue")
		self.colorBox2_13.setStyleSheet("background: cyan")
		self.colorBox2_14.setStyleSheet("background: magenta")
		self.colorBox2_15.setStyleSheet("background: yellow")
		self.colorBox2_16.setStyleSheet("background: rgb(0,128,0)")
		self.colorBox2_17.setStyleSheet("background: rgb(255, 127, 80)")
		self.colorBox2_18.setStyleSheet("background: rgb(148, 0, 211)")
		self.colorBox3_7.setStyleSheet("background: red")
		self.colorBox3_8.setStyleSheet("background: rgb(0,255,0)")
		self.colorBox3_9.setStyleSheet("background: blue")
		self.colorBox3_10.setStyleSheet("background: cyan")
		self.colorBox3_11.setStyleSheet("background: magenta")
		self.colorBox3_12.setStyleSheet("background: yellow")
		self.colorBox4_9.setStyleSheet("background: red")
		self.colorBox4_10.setStyleSheet("background: rgb(0,255,0)")
		self.colorBox4_11.setStyleSheet("background: blue")
		self.colorBox4_12.setStyleSheet("background: cyan")
		self.colorBox4_13.setStyleSheet("background: magenta")
		self.colorBox4_14.setStyleSheet("background: yellow")
		self.colorBox4_15.setStyleSheet("background: rgb(0,128,0)")
		self.colorBox4_16.setStyleSheet("background: rgb(255, 127, 80)")

		#part of re-implementation of dynamic meter/progress bars
		#set meter color
		#self.progressBar.setStyleSheet ("QProgressBar::chunk:%s {background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 				0.5, stop: 0 %s, stop: 1 %s);margin-right: 2px; width: 10px;}" % ("horizontal", "black", "red"))	
		#self.btn = QtGui.QPushButton("Start", self)
		#self.btn.clicked.connect(self.doAction)

	def check_all_changed(self):
		# called when Check All check box is changed - checks all boxes for the relevant jumper/board combo

		if self.checkAllCheckBox1.isChecked():
			self.check1_1.setChecked(True)
			self.check1_2.setChecked(True)
			self.check1_3.setChecked(True)
			self.check1_4.setChecked(True)
			self.check1_5.setChecked(True)
			self.check1_6.setChecked(True)
			self.check1_7.setChecked(True)
			self.check1_8.setChecked(True)
			self.check1_9.setChecked(True)
			self.check1_10.setChecked(True)

		if self.checkAllCheckBox2.isChecked():
			self.check2_1.setChecked(True)
			self.check2_2.setChecked(True)
			self.check2_3.setChecked(True)
			self.check2_4.setChecked(True)
			self.check2_5.setChecked(True)
			self.check2_6.setChecked(True)
			self.check2_7.setChecked(True)
			self.check2_8.setChecked(True)
			self.check2_9.setChecked(True)

		if self.checkAllCheckBox3.isChecked():
			self.check3_1.setChecked(True)
			self.check3_2.setChecked(True)
			self.check3_3.setChecked(True)
			self.check3_4.setChecked(True)
			self.check3_5.setChecked(True)
			self.check3_6.setChecked(True)

		if self.checkAllCheckBox4.isChecked():
			self.check4_1.setChecked(True)
			self.check4_2.setChecked(True)
			self.check4_3.setChecked(True)
			self.check4_4.setChecked(True)
			self.check4_5.setChecked(True)
			self.check4_6.setChecked(True)
			self.check4_7.setChecked(True)
			self.check4_8.setChecked(True)

	def check_box_changed(self):
		# called when check box in New Data tab is changed

		global graphing

		self.check_boxes_new()

		if graphing == True:
			self.timer.stop()
			self.update_graph()

	def check_boxes_new(self):
		# called from check_box_changed - sets box variables to True or False
		# looks at the showing stack widget (based on selected porttype)
		# default is no selected boxes - user can select Check All to choose all boxes

		global porttype, box1, box2, box3, box4, box5, box6, box7, box8, box9, box10, loadedconfig
		box1 = box2 = box3 = box4 = box5 = box6 = box7 = box8 = box9 = box10 = False

		if porttype == '1':
			if self.check1_1.isChecked(): box1 = True
			if self.check1_2.isChecked(): box2 = True
			if self.check1_3.isChecked(): box3 = True
			if self.check1_4.isChecked(): box4 = True
			if self.check1_5.isChecked(): box5 = True
			if self.check1_6.isChecked(): box6 = True
			if self.check1_7.isChecked(): box7 = True
			if self.check1_8.isChecked(): box8 = True
			if self.check1_9.isChecked(): box9 = True
			if self.check1_10.isChecked(): box10 = True

			# see if all checkboxes are checked - set Check All box to checked
			if box1 == box2 == box3 == box4 == box5 == box6 == box7 == box8 == box9 == box10 == True:
				self.checkAllCheckBox1.setChecked(True)
			else:
				self.checkAllCheckBox1.setChecked(False)

		elif porttype == '2':
			if self.check2_1.isChecked(): box1 = True
			if self.check2_2.isChecked(): box2 = True
			if self.check2_3.isChecked(): box3 = True
			if self.check2_4.isChecked(): box4 = True
			if self.check2_5.isChecked(): box5 = True
			if self.check2_6.isChecked(): box6 = True
			if self.check2_7.isChecked(): box7 = True
			if self.check2_8.isChecked(): box8 = True
			if self.check2_9.isChecked(): box9 = True

			# see if all checkboxes are checked - set Check All box to checked
			if box1 == box2 == box3 == box4 == box5 == box6 == box7 == box8 == box9 == True:
				self.checkAllCheckBox2.setChecked(True)
			else:
				self.checkAllCheckBox2.setChecked(False)

		elif porttype == '3':
			if self.check3_1.isChecked(): box1 = True
			if self.check3_2.isChecked(): box2 = True
			if self.check3_3.isChecked(): box3 = True
			if self.check3_4.isChecked(): box4 = True
			if self.check3_5.isChecked(): box5 = True
			if self.check3_6.isChecked(): box6 = True

			# see if all checkboxes are checked - set Check All box to checked
			if box1 == box2 == box3 == box4 == box5 == box6 == True:
				self.checkAllCheckBox3.setChecked(True)
			else:
				self.checkAllCheckBox3.setChecked(False)

		elif porttype == '4':
			if self.check4_1.isChecked(): box1 = True
			if self.check4_2.isChecked(): box2 = True
			if self.check4_3.isChecked(): box3 = True
			if self.check4_4.isChecked(): box4 = True
			if self.check4_5.isChecked(): box5 = True
			if self.check4_6.isChecked(): box6 = True
			if self.check4_7.isChecked(): box7 = True
			if self.check4_8.isChecked(): box8 = True

			# see if all checkboxes are checked - set Check All box to checked
			if box1 == box2 == box3 == box4 == box5 == box6 == box7 == box8 == True:
				self.checkAllCheckBox4.setChecked(True)
			else:
				self.checkAllCheckBox4.setChecked(False)

	def check_boxes_saved(self):
		# sets box variables to True or False - Saved Data tab
		# default is to select all boxes - user can unselect boxes as they choose

		global porttype, box1, box2, box3, box4, box5, box6, box7, box8, box9, box10, showingolddata
		box1 = box2 = box3 = box4 = box5 = box6 = box7 = box8 = box9 = box10 = True

		# set boxes to False that do not exist for each porttype
		if porttype == '2': box10 = False
		elif porttype == '3': box7 = box8 = box9 = box10 = False
		elif porttype == '4': box9 = box10 = False

		# if the box is unchecked, set it to false
		if porttype == '1':
			if not self.check1_11.isChecked(): box1 = False
			if not self.check1_12.isChecked(): box2 = False
			if not self.check1_13.isChecked(): box3 = False
			if not self.check1_14.isChecked(): box4 = False
			if not self.check1_15.isChecked(): box5 = False
			if not self.check1_16.isChecked(): box6 = False
			if not self.check1_17.isChecked(): box7 = False
			if not self.check1_18.isChecked(): box8 = False
			if not self.check1_19.isChecked(): box9 = False
			if not self.check1_20.isChecked(): box10 = False
		elif porttype == '2':
			if not self.check2_10.isChecked(): box1 = False
			if not self.check2_11.isChecked(): box2 = False
			if not self.check2_12.isChecked(): box3 = False
			if not self.check2_13.isChecked(): box4 = False
			if not self.check2_14.isChecked(): box5 = False
			if not self.check2_15.isChecked(): box6 = False
			if not self.check2_16.isChecked(): box7 = False
			if not self.check2_17.isChecked(): box8 = False
			if not self.check2_18.isChecked(): box9 = False
		elif porttype == '3':
			if not self.check3_7.isChecked(): box1 = False
			if not self.check3_8.isChecked(): box2 = False
			if not self.check3_9.isChecked(): box3 = False
			if not self.check3_10.isChecked(): box4 = False
			if not self.check3_11.isChecked(): box5 = False
			if not self.check3_12.isChecked(): box6 = False
		elif porttype == '4':
			if not self.check4_9.isChecked(): box1 = False
			if not self.check4_10.isChecked(): box2 = False
			if not self.check4_11.isChecked(): box3 = False
			if not self.check4_12.isChecked(): box4 = False
			if not self.check4_13.isChecked(): box5 = False
			if not self.check4_14.isChecked(): box6 = False
			if not self.check4_15.isChecked(): box7 = False
			if not self.check4_16.isChecked(): box8 = False

		self.graph_old_data()

	def choose_file_to_write(self):
		# opens file dialog in New Data tab to choose file to write data

		global savefilename, savefilechosen, startsavingdata, stopsavingdata, firsttime

		if self.lineEdit.isVisible():
			self.lineEdit.clear()
			if self.appendRewriteBox.isVisible(): self.appendRewriteBox.hide()

		savefilename = QFileDialog.getSaveFileName(None,"Save File", "/home","CSV (*.csv);;AllFiles(*.*)")

		if savefilename:
			if not savefilename.endswith(".csv"):
				# create warning pop-up window if user does not specify .csv for their save file
				warningmsg = QtGui.QMessageBox.warning(self, "Warning", "You have not selected a .csv file. \n" +
							"For this program to analyze saved data, it must be saved in .csv format.", 
							"Close warning", button1Text="Add .csv extension", defaultButtonNumber=0, 
							escapeButtonNumber=-1)
				
				# if user selects button1 (add .csv extension) - add .csv to savefilename
				if warningmsg == 1:
					savefilename += ".csv"

			savefilechosen = True
			# display savefilename
			self.lineEdit.setText(savefilename)

			self.lineEdit.show()
			self.startSavingStopping.show()
			startsavingdata = False
			stopsavingdata = False
			firsttime = True

		# savefilename was not chosen - file dialog may have been closed before clicking ok
		else: savefilechosen = False

	def choose_saved_file(self):
		# opens file dialog in Saved Data tab to choose file to display

		global filename, oldfilechosen, infinitelinetimer
		error = False

		# if infinitelinetimer is active, stop the timer
		try: self.infinitelinetimer.stop()
		except AttributeError: pass

		# only show files with .csv extension
		filename = QFileDialog.getOpenFileName(None,"Save File", "/home","CSV (*.csv);;AllFiles(*.*)")

		# check to make sure user chose file name before closing file dialog
		if filename: oldfilechosen = True
		else: oldfilechosen = False

		if oldfilechosen == True:
			with open(filename) as csvfile:
				reader = csv.reader(csvfile)
				firstline = next(reader)
				if not firstline[0].startswith("Teensy"):
					# check that file was generated by GUI
					print("ERROR: not a supported data or configuration file")
					error = True
					QtGui.QMessageBox.warning(self, "Error", "This is not a supported data file.",
						QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)

			# if there is no error, call function to display data from this file
			if error == False: self.display_old_data()

	def combo_changed(self):
		# activated when combo box in New Data tab changed - changes StackedWidget by porttype
		# shows the relevant check boxes and lineEdits to display serial data

		global porttype, restart, graphing, showingolddata, startsavingdata, stopsavingdata, newData
		porttype = '0'
		restart = False
		graphing = False
		showingolddata = False
		startsavingdata = False
		stopsavingdata = False

		# stop displaying data if displaying when combo changed
		try: 
			if newData == True: 
				self.stop_data()
				self.displayButton.setText("Display Data")
				self.graphButton.setText("Graph")
		except NameError: pass

		text = self.comboBox.currentText()

		self.graphicsView.clear()
		self.lineEdit.hide()
		self.startSavingStopping.hide()
		self.appendRewriteBox.hide()
		self.appendRewriteBox.setChecked(True)

		if text == "J2 on i.MX8QM":
			porttype = '1'
			self.stackedWidget.show()
			self.stackedWidget.setCurrentIndex(1)

			# set up format for checkboxes and line edits
			self.lineEdit1_1.setReadOnly(True)
			self.lineEdit1_2.setReadOnly(True)
			self.lineEdit1_3.setReadOnly(True)
			self.lineEdit1_4.setReadOnly(True)
			self.lineEdit1_5.setReadOnly(True)
			self.lineEdit1_6.setReadOnly(True)
			self.lineEdit1_7.setReadOnly(True)
			self.lineEdit1_8.setReadOnly(True)
			self.lineEdit1_9.setReadOnly(True)
			self.lineEdit1_10.setReadOnly(True)
			self.lineEdit1_1.clear()
			self.lineEdit1_2.clear()
			self.lineEdit1_3.clear()
			self.lineEdit1_4.clear()
			self.lineEdit1_5.clear()
			self.lineEdit1_6.clear()
			self.lineEdit1_7.clear()
			self.lineEdit1_8.clear()
			self.lineEdit1_9.clear()
			self.lineEdit1_10.clear()
			self.check1_1.setChecked(False)
			self.check1_2.setChecked(False)
			self.check1_3.setChecked(False)
			self.check1_4.setChecked(False)
			self.check1_5.setChecked(False)
			self.check1_6.setChecked(False)
			self.check1_7.setChecked(False)
			self.check1_8.setChecked(False)
			self.check1_9.setChecked(False)
			self.check1_10.setChecked(False)

			self.displayButton.show()
			self.graphButton.show()
			self.chooseFile.show()
			self.plainTextEdit.clear()

			# set range of values for dynamic VU meter from 0 to setMaximum
			#self.progressBar1_1.setMaximum(350)
			#self.progressBar1_2.setMaximum(200)
			#self.progressBar1_3.setMaximum(350)
			#self.progressBar1_4.setMaximum(400)
			#self.progressBar1_5.setMaximum(500)
			#self.progressBar1_6.setMaximum(300)
			#self.progressBar1_7.setMaximum(300)
			#self.progressBar1_8.setMaximum(200)
			#self.progressBar1_9.setMaximum(450)
			#self.progressBar1_10.setMaximum(300)

		elif text == "J3 on i.MX8QM":			
			porttype = '2'
			self.stackedWidget.show()
			self.stackedWidget.setCurrentIndex(2)

			# set up format for checkboxes and line edits
			self.lineEdit2_1.setReadOnly(True)
			self.lineEdit2_2.setReadOnly(True)
			self.lineEdit2_3.setReadOnly(True)
			self.lineEdit2_4.setReadOnly(True)
			self.lineEdit2_5.setReadOnly(True)
			self.lineEdit2_6.setReadOnly(True)
			self.lineEdit2_7.setReadOnly(True)
			self.lineEdit2_8.setReadOnly(True)
			self.lineEdit2_9.setReadOnly(True)
			self.lineEdit2_1.clear()
			self.lineEdit2_2.clear()
			self.lineEdit2_3.clear()
			self.lineEdit2_4.clear()
			self.lineEdit2_5.clear()
			self.lineEdit2_6.clear()
			self.lineEdit2_7.clear()
			self.lineEdit2_8.clear()
			self.lineEdit2_9.clear()
			self.check2_1.setChecked(False)
			self.check2_2.setChecked(False)
			self.check2_3.setChecked(False)
			self.check2_4.setChecked(False)
			self.check2_5.setChecked(False)
			self.check2_6.setChecked(False)
			self.check2_7.setChecked(False)
			self.check2_8.setChecked(False)
			self.check2_9.setChecked(False)

			self.displayButton.show()
			self.graphButton.show()
			self.chooseFile.show()
			self.plainTextEdit.clear()

		elif text == "J2 on i.MX8QXP":
			porttype = '3'
			self.stackedWidget.show()
			self.stackedWidget.setCurrentIndex(3)

			# set up format for checkboxes and line edits
			self.lineEdit3_1.setReadOnly(True)
			self.lineEdit3_2.setReadOnly(True)
			self.lineEdit3_3.setReadOnly(True)
			self.lineEdit3_4.setReadOnly(True)
			self.lineEdit3_5.setReadOnly(True)
			self.lineEdit3_6.setReadOnly(True)
			self.lineEdit3_1.clear()
			self.lineEdit3_2.clear()
			self.lineEdit3_3.clear()
			self.lineEdit3_4.clear()
			self.lineEdit3_5.clear()
			self.lineEdit3_6.clear()
			self.check3_1.setChecked(False)
			self.check3_2.setChecked(False)
			self.check3_3.setChecked(False)
			self.check3_4.setChecked(False)
			self.check3_5.setChecked(False)
			self.check3_6.setChecked(False)

			self.displayButton.show()
			self.graphButton.show()
			self.chooseFile.show()
			self.plainTextEdit.clear()

		elif text == "J3 on i.MX8QXP":
			porttype = '4'
			self.stackedWidget.show()
			self.stackedWidget.setCurrentIndex(4)

			# set up format for checkboxes and line edits
			self.lineEdit4_1.setReadOnly(True)
			self.lineEdit4_2.setReadOnly(True)
			self.lineEdit4_3.setReadOnly(True)
			self.lineEdit4_4.setReadOnly(True)
			self.lineEdit4_5.setReadOnly(True)
			self.lineEdit4_6.setReadOnly(True)
			self.lineEdit4_7.setReadOnly(True)
			self.lineEdit4_8.setReadOnly(True)
			self.lineEdit4_1.clear()
			self.lineEdit4_2.clear()
			self.lineEdit4_3.clear()
			self.lineEdit4_4.clear()
			self.lineEdit4_5.clear()
			self.lineEdit4_6.clear()
			self.lineEdit4_7.clear()
			self.lineEdit4_8.clear()
			self.check4_1.setChecked(False)
			self.check4_2.setChecked(False)
			self.check4_3.setChecked(False)
			self.check4_4.setChecked(False)
			self.check4_5.setChecked(False)
			self.check4_6.setChecked(False)
			self.check4_7.setChecked(False)
			self.check4_8.setChecked(False)

			self.displayButton.show()
			self.graphButton.show()
			self.chooseFile.show()
			self.plainTextEdit.clear()

		else:
			# if no port is selected, hide other widgets
			porttype = '0'
			self.stackedWidget.show()
			self.stackedWidget.setCurrentIndex(0)
			self.displayButton.hide()
			self.graphButton.hide()
			self.chooseFile.hide()
			self.lineEdit.hide()
			self.startSavingStopping.hide()
			self.appendRewriteBox.hide()

#	def doAction(self):
#		# calls progress_bar_value every 1/2 second - for dynamic VU meter
#		# majorly slows down rest of the GUI
#		# part of re-implementation of progress bars
#
#		self.thistimer = QtCore.QTimer()
#		self.thistimer.timeout.connect(self.progress_bar_value)
#		self.thistimer.start(500)

	def display_button_clicked(self):
		# called when display data or stop data button is clicked
		# changes label and functionality depending on action that is being performed

		global timer

		if self.displayButton.text() == "Display Data":
			try:
				# must change button text before display_data starts
				self.displayButton.setText("Stop Data")
				self.display_data()
			except (OSError, IOError) as e: 
				self.displayButton.setText("Display Data")
				print("error - display data - device not connected")
				self.new_data_tab_setup()
				warningmsg = QtGui.QMessageBox.warning(self, "Error", "No device connected at this serial port.",
					QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)
				self.get_ports()

		elif self.displayButton.text() == "Stop Data":
			self.displayButton.setText("Display Data")
			self.graphButton.setText("Graph")
			self.stop_data()

	def display_data(self):
		# called in display_button_clicked - calls read_serial to open serial port

		global newData, porttype, startsavingdata, stopsavingdata, firsttime, graphing, stopsavingwasgraphing

		try:
			if startsavingdata == True:
				newData = True
				self.read_serial()

			elif stopsavingdata == True:
				# if graphing while saving data, resume graphing after stopping
				try:
					if stopsavingwasgraphing == True: 
						graphing = True
				except NameError: pass

				if self.displayButton.text() == "Display Data":
					newData = False
				else:
					newData = True
					self.read_serial()

			else:
				self.set_port_type()
				newData = True
				print("Displaying serial data...")
				self.read_serial()

		except RuntimeError:
			# stops displaying serial data when app is closed (closeEvent)
			print("Stopping data display...")
			return

	def display_old_data(self):
		# called in choose_saved_file - displays saved data in plainTextEdit
		
		global filename, porttype

		self.plainTextEdit_2.clear()
		#self.plainTextEdit_2.setAlignment(QtCore.Qt.AlignJustify)
		
		with open(filename, newline="") as csvfile:
			reader = csv.reader(csvfile)
			firstline = next(reader)
			next(reader)
			variables = next(reader)
			next(reader)
			labels = next(reader)

			porttype = str(variables[0])
		
			for row in reader:
				string = ""
				for i in range(len(row)):
					string += row[i] + " "
				self.plainTextEdit_2.appendPlainText(string)

		self.old_data_layout()

	def get_ports(self):
		# called when getPortButton is clicked - lists available ttyACM serial devices
		# Linux-specific
		
		try: 
			output = subprocess.check_output("ls /dev/ttyACM*", shell=True).decode("utf-8")
			outputlist = output.split("\n")
			outputlist = list(filter(None, outputlist))

			self.serialComboBox.clear()
			self.serialComboBox.addItems(outputlist)

		except (subprocess.CalledProcessError) as e:
			print("no available ports")
			self.serialComboBox.clear()
			self.serialComboBox.addItem("no devices detected")

	def graph_button_clicked(self):
		# called when graph or stop graph button is clicked
		# changes label and functionality depending on action that is being performed

		global timer, graphing, stopsavingwasgraphing

		if self.graphButton.text() == "Graph":

			try:
				if newData == False: 
					print("error - no incoming data to graph")
				else:
					self.update_graph()
					graphing = True
					self.graphButton.setText("Stop Graph")
			except NameError: print("error - no data to graph")

		elif self.graphButton.text() == "Stop Graph":

			try:
				self.timer.stop()
				graphing = False
				stopsavingwasgraphing = False
				self.graphButton.setText("Graph")
			except AttributeError: pass

	def graph_old_data(self):
		# called in old_data_layout and check_boxes_saved - graphs data from Saved Data tab

		global porttype, box1, box2, box3, box4, box5, box6, box7, box8, box9, box10
		global filename, vertlinemoved
		global y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, x

		self.graphicsView.clear()

		x = []
		y1 = []
		y2 = []
		y3 = []
		y4 = []
		y5 = []
		y6 = []
		y7 = []
		y8 = []
		y9 = []
		y10 = []

		with open(filename, newline="") as csvfile:
			reader = csv.reader(csvfile)
			firstline = next(reader)
			next(reader)
			variables = next(reader)
			next(reader)
			labels = next(reader)

			countlength = 0

			for row in reader:
				countlength += 1
				y1.append(int(row[1]))
				y2.append(int(row[2]))
				y3.append(int(row[3]))
				y4.append(int(row[4]))
				y5.append(int(row[5]))
				y6.append(int(row[6]))

				if porttype == '1':
					y7.append(int(row[7]))
					y8.append(int(row[8]))
					y9.append(int(row[9]))
					y10.append(int(row[10]))
				if porttype == '2':
					y7.append(int(row[7]))
					y8.append(int(row[8]))
					y9.append(int(row[9]))
				if porttype == '4':
					y7.append(int(row[7]))
					y8.append(int(row[8]))

		x = list(range(0,countlength))

		self.if_true()
	
		# if box is unchecked, clear the graph and re-call method to draw lines
		if box1 == False:
			self.graphicsView.clear()
			self.if_true()
		if box2 == False:
			self.graphicsView.clear()
			self.if_true()
		if box3 == False:
			self.graphicsView.clear()
			self.if_true()
		if box4 == False:
			self.graphicsView.clear()
			self.if_true()
		if box5 == False:
			self.graphicsView.clear()
			self.if_true()
		if box6 == False:
			self.graphicsView.clear()
			self.if_true()

		if porttype == '1':
			if box7 == False:
				self.graphicsView.clear()
				self.if_true()
			if box8 == False:
				self.graphicsView.clear()
				self.if_true()
			if box9 == False:
				self.graphicsView.clear()
				self.if_true()
			if box10 == False:
				self.graphicsView.clear()
				self.if_true()
		if porttype == '2':
			if box7 == False:
				self.graphicsView.clear()
				self.if_true()
			if box8 == False:
				self.graphicsView.clear()
				self.if_true()
			if box9 == False:
				self.graphicsView.clear()
				self.if_true()
		if porttype == '4':
			if box7 == False:
				self.graphicsView.clear()
				self.if_true()
			if box8 == False:
				self.graphicsView.clear()
				self.if_true()

	def if_true(self):
		# called in display_old_data - redraws graph when plots are turned on and off

		global box1, box2, box3, box4, box5, box6, box7, box8, box9, box10
		global y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, vertline
		global linenumberold, infinitelinetimer, linenumber

		try:
			# if line number is defined, draw line in same place as line number (after graph cleared)
			vertline = self.graphicsView.plotItem.addLine(linenumber,90,None,movable=True,bounds=[0,len(y1)-1])

		except NameError:
			# if line number is not defined, first time - draw line at end of data
			vertline = self.graphicsView.plotItem.addLine(len(y1)-1,90,None,movable=True,bounds=[0,len(y1)-1])

		linenumberold = len(y1)-1

		# if box is checked, draw corresponding line
		if box1 == True: curve1 = self.graphicsView.plotItem.plot(x, y1, pen=pyqtgraph.mkPen('r'))
		if box2 == True: curve2 = self.graphicsView.plotItem.plot(x, y2, pen=pyqtgraph.mkPen('g'))
		if box3 == True: curve3 = self.graphicsView.plotItem.plot(x, y3, pen=pyqtgraph.mkPen('b'))
		if box4 == True: curve4 = self.graphicsView.plotItem.plot(x, y4, pen=pyqtgraph.mkPen('c'))
		if box5 == True: curve5 = self.graphicsView.plotItem.plot(x, y5, pen=pyqtgraph.mkPen('m'))
		if box6 == True: curve6 = self.graphicsView.plotItem.plot(x, y6, pen=pyqtgraph.mkPen('y'))
		if box7 == True: curve7 = self.graphicsView.plotItem.plot(x, y7, pen=pyqtgraph.mkPen(0,128,0))
		if box8 == True: curve8 = self.graphicsView.plotItem.plot(x, y8, pen=pyqtgraph.mkPen(255, 127, 80))
		if box9 == True: curve9 = self.graphicsView.plotItem.plot(x, y9, pen=pyqtgraph.mkPen(148, 0, 211))
		if box10 == True: curve10 = self.graphicsView.plotItem.plot(x, y10, pen=pyqtgraph.mkPen(165, 42, 42))

		# check infiniteline position every second (1000 ms)
		self.infinitelinetimer = QtCore.QTimer()
		self.infinitelinetimer.timeout.connect(self.infinite_line_position)
		self.infinitelinetimer.start(1000)

	def infinite_line_position(self):
		# called in if_true - creates infinite line in Saved Data plot that can be moved
		# sets lineEdit text to the values at the infinite line

		global linenumberold, linenumber, porttype

		linenumber = int(round(vertline.value()))

		# highlight line
		yellowformat = QTextBlockFormat()
		yellowformat.setBackground(Qt.yellow)

		# un-highlight line
		clearformat = QTextBlockFormat()
		clearformat.clearBackground()

		if not linenumberold == linenumber:
			# if infinite line has moved, clear the highlighted format before moving the cursor
			cursor = QTextCursor(self.plainTextEdit_2.document().findBlockByNumber(linenumberold))
			cursor.setBlockFormat(clearformat)

		cursor = QTextCursor(self.plainTextEdit_2.document().findBlockByNumber(linenumber))
		cursor.setBlockFormat(yellowformat)

		self.plainTextEdit_2.setTextCursor(cursor)
		self.plainTextEdit_2.setCenterOnScroll(True)
		self.plainTextEdit_2.centerOnScroll()

		linenumberold = linenumber

		text = self.plainTextEdit_2.toPlainText()
		plainTextData = text.split("\n")

		splitTextData = plainTextData[linenumber].split()

		if porttype == '1':
			self.lineEdit1_2_1.setText(splitTextData[1])
			self.lineEdit1_2_2.setText(splitTextData[2])
			self.lineEdit1_2_3.setText(splitTextData[3])
			self.lineEdit1_2_4.setText(splitTextData[4])
			self.lineEdit1_2_5.setText(splitTextData[5])
			self.lineEdit1_2_6.setText(splitTextData[6])
			self.lineEdit1_2_7.setText(splitTextData[7])
			self.lineEdit1_2_8.setText(splitTextData[8])
			self.lineEdit1_2_9.setText(splitTextData[9])
			self.lineEdit1_2_10.setText(splitTextData[10])

		if porttype == '2':
			self.lineEdit2_2_1.setText(splitTextData[1])
			self.lineEdit2_2_2.setText(splitTextData[2])
			self.lineEdit2_2_3.setText(splitTextData[3])
			self.lineEdit2_2_4.setText(splitTextData[4])
			self.lineEdit2_2_5.setText(splitTextData[5])
			self.lineEdit2_2_6.setText(splitTextData[6])
			self.lineEdit2_2_7.setText(splitTextData[7])
			self.lineEdit2_2_8.setText(splitTextData[8])
			self.lineEdit2_2_9.setText(splitTextData[9])

		if porttype == '3':
			self.lineEdit3_2_1.setText(splitTextData[1])
			self.lineEdit3_2_2.setText(splitTextData[2])
			self.lineEdit3_2_3.setText(splitTextData[3])
			self.lineEdit3_2_4.setText(splitTextData[4])
			self.lineEdit3_2_5.setText(splitTextData[5])
			self.lineEdit3_2_6.setText(splitTextData[6])

		if porttype == '4':
			self.lineEdit4_2_1.setText(splitTextData[1])
			self.lineEdit4_2_2.setText(splitTextData[2])
			self.lineEdit4_2_3.setText(splitTextData[3])
			self.lineEdit4_2_4.setText(splitTextData[4])
			self.lineEdit4_2_5.setText(splitTextData[5])
			self.lineEdit4_2_6.setText(splitTextData[6])
			self.lineEdit4_2_7.setText(splitTextData[7])
			self.lineEdit4_2_8.setText(splitTextData[8])

	def load_config(self):
		# activated if LoadConfig is clicked - loads a previous configuration file

		global configfilename, configfilechosen, loadedconfig, startsavingdata, stopsavingdata
		global porttype, box1, box2, box3, box4, box5, box6, box7, box8, box9, box10
		error = False

		configfilename = QFileDialog.getOpenFileName(None,"Open Config File", "/home","CSV(*.csv);;AllFiles(*.*)")

		if configfilename:
			configfilechosen = True
			loadedconfig = True
			startsavingdata = False
			stopsavingdata = False
		else:
			configfilechosen = False

		if configfilechosen == True:
			with open(configfilename) as csvfile:
				reader = csv.reader(csvfile)
				firstline = next(reader)
				if not firstline[0].startswith("Teensy"):
					# check that file was generated by GUI
					print("ERROR: not a supported data or configuration file")
					error = True
					QtGui.QMessageBox.warning(self, "Error", "This is not a supported configuration file.",
						QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)

				next(reader)
				config = next(reader)

			if error == False:
				porttype = config[0]
				box1 = config[1]
				box2 = config[2]
				box3 = config[3]
				box4 = config[4]
				box5 = config[5]
				box6 = config[6]
				box7 = config[7]
				box8 = config[8]
				box9 = config[9]
				box10 = config[10]

			self.displayButton.show()
			self.graphButton.show()
			self.chooseFile.show()

			porttype = str(porttype)

			# transform strings to booleans
			if box1 == "True": box1 = True
			elif box1 == "False": box1 = False
			if box2 == "True": box2 = True
			elif box2 == "False": box2 = False
			if box3 == "True": box3 = True
			elif box3 == "False": box3 = False
			if box4 == "True": box4 = True
			elif box4 == "False": box4 = False
			if box5 == "True": box5 = True
			elif box5 == "False": box5 = False
			if box6 == "True": box6 = True
			elif box6 == "False": box6 = False
			if box7 == "True": box7 = True
			elif box7 == "False": box7 = False
			if box8 == "True": box8 = True
			elif box8 == "False": box8 = False
			if box9 == "True": box9 = True
			elif box9 == "False": box9 = False
			if box10 == "True": box10 = True
			elif box10 == "False": box10 = False

			if porttype == '1': self.comboBox.setCurrentIndex(1)
			elif porttype == '2': self.comboBox.setCurrentIndex(2)
			elif porttype == '3': self.comboBox.setCurrentIndex(3)
			elif porttype == '4': self.comboBox.setCurrentIndex(4)

			self.set_checked_load()

	def max_clicked(self):
		# called when maxButton clicked - sets update rate to maximum speed (10 ms)

		global ser, updaterate
	
		ser = serial.Serial()
		ser.baudrate = 115200

		acmport = self.serialComboBox.currentText()

		if acmport in ("no devices detected", ""):
			print("no devices detected")
		else:
			ser.port = acmport
			ser.open()
			ser.flushInput()
			ser.flushOutput()
			ser.write(b'_')
			time.sleep(0.1)
			ser.flushOutput() # flush input and output to clear everything
			ser.flushInput()  # before changing state

			updaterate = 10
			self.updateRateLineEdit.setText(str(updaterate) + "ms")

	def minus_clicked(self):
		# called when minusButton clicked - decreases current update rate by 10 ms

		global ser, updaterate	
	
		ser = serial.Serial()
		ser.baudrate = 115200

		acmport = self.serialComboBox.currentText()

		if acmport in ("no devices detected", ""):
			print("no devices detected")
		else:
			ser.port = acmport
			ser.open()
			ser.flushInput()
			ser.flushOutput()
			ser.write(b'+')
			time.sleep(0.1)
			ser.flushOutput() # flush input and output to clear everything
			ser.flushInput()  # before changing state

			if updaterate < 1000:
				updaterate = updaterate + 10
				self.updateRateLineEdit.setText(str(updaterate) + "ms")

	def min_clicked(self):
		# called when minButton clicked - sets update rate to minimum speed (1000 ms)

		global ser, updaterate	
	
		ser = serial.Serial()
		ser.baudrate = 115200

		acmport = self.serialComboBox.currentText()

		if acmport in ("no devices detected", ""):
			print("no devices detected")
		else:
			ser.port = acmport
			ser.open()
			ser.flushInput()
			ser.flushOutput()
			ser.write(b'-')
			time.sleep(0.1)
			ser.flushOutput() # flush input and output to clear everything
			ser.flushInput()  # before changing state

			updaterate = 1000
			self.updateRateLineEdit.setText(str(updaterate) + "ms")

	def new_data_tab_setup(self):
		# called when New Data tab is clicked - hides and clears widgets

		self.graphicsView.clear()
		self.plainTextEdit.clear()

		self.stackedWidget.show()
		self.comboBox.setCurrentIndex(0)

		self.plainTextEdit.hide()
		self.displayButton.hide()
		self.graphButton.hide()
	
		self.chooseFile.hide()
		self.lineEdit.hide()
		self.startSavingStopping.hide()
		self.appendRewriteBox.hide()
		self.appendRewriteBox.setChecked(True)

	def old_data_layout(self):
		# called in display_old_data - sets up Saved Data tab based on porttype and data from file

		global porttype, showingolddata

		showingolddata = True

		if porttype == '1':
			self.stackedWidget_3.show()
			self.stackedWidget_3.setCurrentIndex(1)
			self.label.show()
			self.label.setText("J2 on i.MX8QM")
			self.label.setAlignment(QtCore.Qt.AlignCenter)

			self.check1_11.setChecked(True)
			self.check1_12.setChecked(True)
			self.check1_13.setChecked(True)
			self.check1_14.setChecked(True)
			self.check1_15.setChecked(True)
			self.check1_16.setChecked(True)
			self.check1_17.setChecked(True)
			self.check1_18.setChecked(True)
			self.check1_19.setChecked(True)
			self.check1_20.setChecked(True)
			self.lineEdit1_2_1.setReadOnly(True)
			self.lineEdit1_2_2.setReadOnly(True)
			self.lineEdit1_2_3.setReadOnly(True)
			self.lineEdit1_2_4.setReadOnly(True)
			self.lineEdit1_2_5.setReadOnly(True)
			self.lineEdit1_2_6.setReadOnly(True)
			self.lineEdit1_2_7.setReadOnly(True)
			self.lineEdit1_2_8.setReadOnly(True)
			self.lineEdit1_2_9.setReadOnly(True)
			self.lineEdit1_2_10.setReadOnly(True)
			self.check1_11.stateChanged.connect(self.check_boxes_saved)
			self.check1_12.stateChanged.connect(self.check_boxes_saved)
			self.check1_13.stateChanged.connect(self.check_boxes_saved)
			self.check1_14.stateChanged.connect(self.check_boxes_saved)
			self.check1_15.stateChanged.connect(self.check_boxes_saved)
			self.check1_16.stateChanged.connect(self.check_boxes_saved)
			self.check1_17.stateChanged.connect(self.check_boxes_saved)
			self.check1_18.stateChanged.connect(self.check_boxes_saved)
			self.check1_19.stateChanged.connect(self.check_boxes_saved)
			self.check1_20.stateChanged.connect(self.check_boxes_saved)

		elif porttype == '2':
			self.stackedWidget_3.show()
			self.stackedWidget_3.setCurrentIndex(2)
			self.label.show()
			self.label.setText("J3 on i.MX8QM")
			self.label.setAlignment(QtCore.Qt.AlignCenter)

			self.check2_10.setChecked(True)
			self.check2_11.setChecked(True)
			self.check2_12.setChecked(True)
			self.check2_13.setChecked(True)
			self.check2_14.setChecked(True)
			self.check2_15.setChecked(True)
			self.check2_16.setChecked(True)
			self.check2_17.setChecked(True)
			self.check2_18.setChecked(True)
			self.lineEdit2_2_1.setReadOnly(True)
			self.lineEdit2_2_2.setReadOnly(True)
			self.lineEdit2_2_3.setReadOnly(True)
			self.lineEdit2_2_4.setReadOnly(True)
			self.lineEdit2_2_5.setReadOnly(True)
			self.lineEdit2_2_6.setReadOnly(True)
			self.lineEdit2_2_7.setReadOnly(True)
			self.lineEdit2_2_8.setReadOnly(True)
			self.lineEdit2_2_9.setReadOnly(True)
			self.check2_10.stateChanged.connect(self.check_boxes_saved)
			self.check2_11.stateChanged.connect(self.check_boxes_saved)
			self.check2_12.stateChanged.connect(self.check_boxes_saved)
			self.check2_13.stateChanged.connect(self.check_boxes_saved)
			self.check2_14.stateChanged.connect(self.check_boxes_saved)
			self.check2_15.stateChanged.connect(self.check_boxes_saved)
			self.check2_16.stateChanged.connect(self.check_boxes_saved)
			self.check2_17.stateChanged.connect(self.check_boxes_saved)
			self.check2_18.stateChanged.connect(self.check_boxes_saved)

		elif porttype == '3':
			self.stackedWidget_3.show()
			self.stackedWidget_3.setCurrentIndex(3)
			self.label.show()
			self.label.setText("J2 on i.MX8QXP")
			self.label.setAlignment(QtCore.Qt.AlignCenter)

			self.check3_7.setChecked(True)
			self.check3_8.setChecked(True)
			self.check3_9.setChecked(True)
			self.check3_10.setChecked(True)
			self.check3_11.setChecked(True)
			self.check3_12.setChecked(True)
			self.lineEdit3_2_1.setReadOnly(True)
			self.lineEdit3_2_2.setReadOnly(True)
			self.lineEdit3_2_3.setReadOnly(True)
			self.lineEdit3_2_4.setReadOnly(True)
			self.lineEdit3_2_5.setReadOnly(True)
			self.lineEdit3_2_6.setReadOnly(True)
			self.check3_7.stateChanged.connect(self.check_boxes_saved)
			self.check3_8.stateChanged.connect(self.check_boxes_saved)
			self.check3_9.stateChanged.connect(self.check_boxes_saved)
			self.check3_10.stateChanged.connect(self.check_boxes_saved)
			self.check3_11.stateChanged.connect(self.check_boxes_saved)
			self.check3_12.stateChanged.connect(self.check_boxes_saved)

		elif porttype == '4':
			self.stackedWidget_3.show()
			self.stackedWidget_3.setCurrentIndex(4)
			self.label.show()
			self.label.setText("J3 on i.MX8QXP")
			self.label.setAlignment(QtCore.Qt.AlignCenter)

			self.check4_9.setChecked(True)
			self.check4_10.setChecked(True)
			self.check4_11.setChecked(True)
			self.check4_12.setChecked(True)
			self.check4_13.setChecked(True)
			self.check4_14.setChecked(True)
			self.check4_15.setChecked(True)
			self.check4_16.setChecked(True)
			self.lineEdit4_2_1.setReadOnly(True)
			self.lineEdit4_2_2.setReadOnly(True)
			self.lineEdit4_2_3.setReadOnly(True)
			self.lineEdit4_2_4.setReadOnly(True)
			self.lineEdit4_2_5.setReadOnly(True)
			self.lineEdit4_2_6.setReadOnly(True)
			self.lineEdit4_2_7.setReadOnly(True)
			self.lineEdit4_2_8.setReadOnly(True)
			self.check4_9.stateChanged.connect(self.check_boxes_saved)
			self.check4_10.stateChanged.connect(self.check_boxes_saved)
			self.check4_11.stateChanged.connect(self.check_boxes_saved)
			self.check4_12.stateChanged.connect(self.check_boxes_saved)
			self.check4_13.stateChanged.connect(self.check_boxes_saved)
			self.check4_14.stateChanged.connect(self.check_boxes_saved)
			self.check4_15.stateChanged.connect(self.check_boxes_saved)
			self.check4_16.stateChanged.connect(self.check_boxes_saved)

		self.check_boxes_saved()
		self.graph_old_data()

	def plus_clicked(self):
		# called when plusButton clicked - increases current update rate by 10 ms

		global ser, updaterate	
	
		ser = serial.Serial()
		ser.baudrate = 115200

		acmport = self.serialComboBox.currentText()

		if acmport in ("no devices detected", ""):
			print("no devices detected")
		else:
			ser.port = acmport
			ser.open()
			ser.flushInput()
			ser.flushOutput()
			ser.write(b'=')
			time.sleep(0.1)
			ser.flushOutput() # flush input and output to clear everything
			ser.flushInput()  # before changing state

			if updaterate > 10:
				updaterate = updaterate - 10
				self.updateRateLineEdit.setText(str(updaterate) + "ms")

#	def progress_bar_value(self):
#		# dynamic VU meter bar graphs
#		# majorly slows down the rest of the GUI
#		# to re-implement, must add QProgressBar widgets back into QT Developer UI file
#
#		text = self.plainTextEdit.toPlainText()
#		dataArray = text.split("\n")
#
#		for eachLine in dataArray:
#			if len(eachLine) > 1:
#				dataLines = eachLine.split(' ')
#				dataLines = list(filter(None, dataLines))
#
#				if porttype == '1':
#					self.progressBar1_1.setValue(int(dataLines[1]))
#					self.progressBar1_2.setValue(int(dataLines[2]))
#					self.progressBar1_3.setValue(int(dataLines[3]))
#					self.progressBar1_4.setValue(int(dataLines[4]))
#					self.progressBar1_5.setValue(int(dataLines[5]))
#					self.progressBar1_6.setValue(int(dataLines[6]))
#					self.progressBar1_7.setValue(int(dataLines[7]))
#					self.progressBar1_8.setValue(int(dataLines[8]))
#					self.progressBar1_9.setValue(int(dataLines[9]))
#					self.progressBar1_10.setValue(int(dataLines[10]))
#				if porttype == '2':
#					self.progressBar2_1.setValue(int(dataLines[1]))
#					self.progressBar2_2.setValue(int(dataLines[2]))
#					self.progressBar2_3.setValue(int(dataLines[3]))
#					self.progressBar2_4.setValue(int(dataLines[4]))
#					self.progressBar2_5.setValue(int(dataLines[5]))
#					self.progressBar2_6.setValue(int(dataLines[6]))
#					self.progressBar2_7.setValue(int(dataLines[7]))
#					self.progressBar2_8.setValue(int(dataLines[8]))
#					self.progressBar2_9.setValue(int(dataLines[9]))
#				if porttype == '3':
#					self.progressBar3_1.setValue(int(dataLines[1]))
#					self.progressBar3_2.setValue(int(dataLines[2]))
#					self.progressBar3_3.setValue(int(dataLines[3]))
#					self.progressBar3_4.setValue(int(dataLines[4]))
#					self.progressBar3_5.setValue(int(dataLines[5]))
#					self.progressBar3_6.setValue(int(dataLines[6]))
#				if porttype == '4':
#					self.progressBar4_1.setValue(int(dataLines[1]))
#					self.progressBar4_2.setValue(int(dataLines[2]))
#					self.progressBar4_3.setValue(int(dataLines[3]))
#					self.progressBar4_4.setValue(int(dataLines[4]))
#					self.progressBar4_5.setValue(int(dataLines[5]))
#					self.progressBar4_6.setValue(int(dataLines[6]))
#					self.progressBar4_7.setValue(int(dataLines[7]))
#					self.progressBar4_8.setValue(int(dataLines[8]))

	def read_serial(self):
		# opens serial port and sends it the values for the porttpe
		# displays this data in a hidden QPlainTextEdit
		# writes data to CSV file if Start Saving Data clicked and file chosen

		global ser, yar1, startsavingdata, savefilename, graphing, stopsavingdata, firsttime
	
		ser = serial.Serial()
		ser.baudrate = 115200
	
		acmport = self.serialComboBox.currentText()
		ser.port = acmport

		ser.open()
		ser.flushInput()
		ser.flushOutput()

		if startsavingdata == False:
			if stopsavingdata == False:
				#ser.write(b'R') # reset profiler 
				#time.sleep(0.25)
				#ser.write(b'd') # turn off delay for faster input
				#time.sleep(0.25)
				#ser.write(b'c') # turn on chart mode
				#time.sleep(0.25)
				ser.write(b'G') # put in GUI mode (\x47)
				time.sleep(0.5)

		ser.flushOutput() # flush input and output to clear everything
		ser.flushInput()  # before changing state
		ser.readline() # read first line as it may be incomplete 
	
		if startsavingdata == True:
			# write data to file if startSavingData was clicked

			with open(savefilename, 'a', newline="") as output_file:

				# if graphing before start saving clicked, keep graphing after clicked
				if graphing == True:
					self.update_graph()
			
				starttime = time.time()
				while ser.isOpen() == True:	
					writer = csv.writer(output_file)
					x = ser.readline()

					# ignore any line read that is not in the proper format
					if x.decode().startswith(("0 ","1 ","2 ","3 ")):
						stdout.write(x.decode())
						linelist = x.decode().split()
						currenttime = time.time() - starttime
						linelist.append(currenttime)
						writer.writerow(linelist)
						self.plainTextEdit.appendPlainText(x.decode())
						QtGui.QApplication.processEvents()

					stdout.flush()

					self.text_display()
					#self.progress_bar_value()

			if stopsavingdata == True: self.display_data()

			stopsavingdata = False

		else: # if not saving data

			if graphing == True: self.update_graph()

			while ser.isOpen() == True:	

				x = ser.readline()

				# ignore any line read that is not in the proper format
				if x.decode().startswith(("0 ","1 ","2 ","3 ")):
					stdout.write(x.decode())
					self.plainTextEdit.appendPlainText(x.decode())
					QtGui.QApplication.processEvents()

				stdout.flush()
				self.text_display()
				#self.progress_bar_value()

	def saved_data_tab_setup(self):
		# called when Saved Data tab is clicked - hides and clears widgets

		self.graphicsView.clear()
		self.plainTextEdit_2.clear()

		self.label.hide()
		self.stackedWidget_3.show()
		self.stackedWidget_3.setCurrentIndex(0)

	def serial_combo_changed(self):
		# called when serialComboBox is changed - resets to default tab set up
		# calls max_clicked to force the starting update rate to its maximum 

		global updaterate, newData, ser

		updaterate = 0

		self.new_data_tab_setup()

		try:
			if self.serialComboBox.currentText().startswith("/dev/ttyACM"):
				self.updateRateLineEdit.clear()
				self.max_clicked()
				ser.close()

		except OSError:
			print("error - resource busy")

			if not self.serialComboBox.currentText().endswith("busy"):
				text = self.serialComboBox.currentText()
				self.serialComboBox.removeItem(self.serialComboBox.currentIndex())
				self.serialComboBox.insertItem(0, text + " - resource busy")

		except (subprocess.CalledProcessError) as e:
			print("no available ports")
			self.serialComboBox.clear()
			self.serialComboBox.addItem("no devices detected")

	def set_checked_load(self):
		# set check boxes as checked according to loaded configuration file

		global porttype, box1, box2, box3, box4, box5, box6, box7, box8, box9, box10
		
		if porttype == '1':
			if box1 == True: self.check1_1.setChecked(True)
			if box2 == True: self.check1_2.setChecked(True)
			if box3 == True: self.check1_3.setChecked(True)
			if box4 == True: self.check1_4.setChecked(True)
			if box5 == True: self.check1_5.setChecked(True)
			if box6 == True: self.check1_6.setChecked(True)
			if box7 == True: self.check1_7.setChecked(True)
			if box8 == True: self.check1_8.setChecked(True)
			if box9 == True: self.check1_9.setChecked(True)
			if box10 == True: self.check1_10.setChecked(True)
		if porttype == '2':
			if box1 == True: self.check2_1.setChecked(True)
			if box2 == True: self.check2_2.setChecked(True)
			if box3 == True: self.check2_3.setChecked(True)
			if box4 == True: self.check2_4.setChecked(True)
			if box5 == True: self.check2_5.setChecked(True)
			if box6 == True: self.check2_6.setChecked(True)
			if box7 == True: self.check2_7.setChecked(True)
			if box8 == True: self.check2_8.setChecked(True)
			if box9 == True: self.check2_9.setChecked(True)
		if porttype == '3':
			if box1 == True: self.check3_1.setChecked(True)
			if box2 == True: self.check3_2.setChecked(True)
			if box3 == True: self.check3_3.setChecked(True)
			if box4 == True: self.check3_4.setChecked(True)
			if box5 == True: self.check3_5.setChecked(True)
			if box6 == True: self.check3_6.setChecked(True)
		if porttype == '4':
			if box1 == True: self.check4_1.setChecked(True)
			if box2 == True: self.check4_2.setChecked(True)
			if box3 == True: self.check4_3.setChecked(True)
			if box4 == True: self.check4_4.setChecked(True)
			if box5 == True: self.check4_5.setChecked(True)
			if box6 == True: self.check4_6.setChecked(True)
			if box7 == True: self.check4_7.setChecked(True)
			if box8 == True: self.check4_8.setChecked(True)

		self.check_boxes_new()

	def set_port_type(self):
		# send porttype to device

		global ser, porttype	
	
		ser = serial.Serial()
		ser.baudrate = 115200

		acmport = self.serialComboBox.currentText()
		ser.port = acmport

		ser.open()
		ser.flushInput()
		ser.flushOutput()
		ser.write(porttype.encode()) # choose porttype
		time.sleep(0.5)

		if porttype == '1':
			ser.write(b'!') # ensure changed to option 1
			time.sleep(0.5)
		if porttype == '2':
			ser.write(b'@') # ensure changed to option 2
			time.sleep(0.5)
		if porttype == '3':
			ser.write(b'#') # ensure changed to option 3
			time.sleep(0.5)
		if porttype == '4':
			ser.write(b'$') # ensure changed to option 4
			time.sleep(0.5)

		ser.flushOutput() # flush input and output to clear everything
		ser.flushInput()  # before changing state

	def start_or_stop_saving_data(self):
		# called when start or stop saving data is clicked - dictates whether to start or stop

		global startsavingdata, firsttime

		if self.startSavingStopping.text() == "Start Saving Data": self.start_saving_data()
		else: self.stop_saving_data()

	def start_saving_data(self):
		# called from start_or_stop - saves data to csv file
		# if first time, writes header to document; if not, skips header and appends data

		global porttype, box1, box2, box3, box4, box5, box6, box7, box8, box9, box10, savefilechosen
		global startsavingdata, newData, stopsavingdata, firsttime, ser, updaterate
		stopsavingdata = False
		error = False

		# newData - serial port is open and displaying data
		if not "newData" in globals():
			error = True
			QtGui.QMessageBox.warning(self, "Error", "There is no incoming data to save.",
				QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)
			print("error - no new data to save")
		else:
			if newData == False:
				error = True
				QtGui.QMessageBox.warning(self, "Error", "There is no incoming data to save.",
					QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)
				print("error - no new data to save")

		if error == False:

			startsavingdata = True
			self.startSavingStopping.setText("Stop Saving Data")

			print("Starting saving data...")

			if firsttime == True: 

				self.check_boxes_new()

				# write header to CSV to set up file - first time startSavingData clicked
				header_string = ["Teensy GUI Data File", datetime.date.today()]
				header_info = [porttype, box1, box2, box3, box4, box5, box6, box7, box8, box9,
						 box10, savefilename]
				header_labels = []

				if savefilename.endswith(".csv"):
					# if savedfilename ends with .csv, remove and add config file ending
					stripped = savefilename[:-4]
					newconfigfilename = stripped + "_config.csv"
				else:
					newconfigfilename = savefilename + "_config.csv"

				# write single byte to serial device to create output of labels (from Teensy source code)
				ser.write(b"L")
				ser.close()
				ser.open()

				raillabels = []
				labels = []

				timeout_start = time.time()

				if ser.isOpen() == True:
					# takes longer for slower update rates
					if updaterate > 100:
						timeout = 1.5
					else:
						timeout = 0.5
					while time.time() < timeout_start + timeout:
						x = ser.readline()
						if not x.startswith((b"0", b"1", b"2", b"3", b"*")):
							if x.startswith((b"J2", b"J3")):
								header = x.decode()
							else:
								labels.append(x.decode().strip().split())

				labels = list(filter(None, labels))
				for item in range(len(labels)):
					raillabels.append(labels[item][0])

				if porttype == '1':
					# "SW_MAIN", "SW_CPUA53", "SW_CPUA72", "SW_GPU0", "SW_GPU1", "SW_MEMC", 
					#"SW_DDRIO0", "SW_DDRIO1", "SW_3P3", "SW_1P8"
					header_labels.append("port")
					header_labels.extend(raillabels)
					header_labels.append("time")

				elif porttype == '2':
					# "LDO_SCU1P8", "LDO_SD1", "LDO_SD2", "SW_3P3_SD1", "SW_3P3_SD2", "LDO_SIM", 
					# "LDO_2P5", "LDO_1P2", "P5V0"
					header_labels.append("port")
					header_labels.extend(raillabels)
					header_labels.append("time")

				elif porttype == '3':
					# "VDD_MAIN", "VDD_CPU", "VDD_GPU", "VDD_DDRIO", "VDD_SW3V3", "VDD_SW1V8"

					header_labels.append("port")
					header_labels.extend(raillabels)
					header_labels.append("time")

				elif porttype == '4':
					# "LDO_SCU1V8", "LDO_SD1", "LDO_SD2", "SD1_SPWR", "LDO_S", "LDO_2V5", 
					# "LDO_1V2", "P5V0"

					header_labels.append("port")
					header_labels.extend(raillabels)
					header_labels.append("time")

				with open(savefilename, 'w', newline="") as output_file:
					# rewriting file with proper configuration
					writer = csv.writer(output_file)
					writer.writerow(header_string)
					writer.writerow("")
					writer.writerow(header_info)
					writer.writerow("")
					writer.writerow(header_labels)

				with open(newconfigfilename, 'w', newline="") as config_file:
					# creating and writing and separate config file 
					writer = csv.writer(config_file)
					writer.writerow(header_string)
					writer.writerow("")
					writer.writerow(header_info)
					writer.writerow("")
					writer.writerow(header_labels)

			if self.appendRewriteBox.isChecked() == False:
				# if append box is unchecked, rewrite header to CSV to override existing file

				header_string = ["Teensy GUI Data File", datetime.date.today()]
				header_info = [porttype, box1, box2, box3, box4, box5, box6, box7, box8, box9,
						 box10, savefilename]
				header_labels = []

				# write single byte to serial device to create output of labels (from Teensy source code)
				ser.write(b"L")
				ser.close()
				ser.open()

				raillabels = []
				labels = []

				timeout_start = time.time()

				if ser.isOpen() == True:
					# takes longer for slower update rates
					if updaterate > 100:
						timeout = 1.5
					else:
						timeout = 0.5
					while time.time() < timeout_start + timeout:
						x = ser.readline()
						if not x.startswith((b"0", b"1", b"2", b"3", b"*")):
							if x.startswith((b"J2", b"J3")):
								header = x.decode()
							else:
								labels.append(x.decode().strip().split())

				labels = list(filter(None, labels))
				for item in range(len(labels)):
					raillabels.append(labels[item][0])

				if porttype == '1':
					# "SW_MAIN", "SW_CPUA53", "SW_CPUA72", "SW_GPU0", "SW_GPU1", "SW_MEMC", 
					# "SW_DDRIO0", "SW_DDRIO1", "SW_3P3", "SW_1P8"
					header_labels.append("port")
					header_labels.extend(raillabels)
					header_labels.append("time")

				elif porttype == '2':
					# "LDO_SCU1P8", "LDO_SD1", "LDO_SD2", "SW_3P3_SD1", "SW_3P3_SD2", "LDO_SIM", 
					# "LDO_2P5", "LDO_1P2", "P5V0"
					header_labels.append("port")
					header_labels.extend(raillabels)
					header_labels.append("time")

				elif porttype == '3':
					# "VDD_MAIN", "VDD_CPU", "VDD_GPU", "VDD_DDRIO", "VDD_SW3V3", "VDD_SW1V8"

					header_labels.append("port")
					header_labels.extend(raillabels)
					header_labels.append("time")

				elif porttype == '4':
					# "LDO_SCU1V8", "LDO_SD1", "LDO_SD2", "SD1_SPWR", "LDO_S", "LDO_2V5", 
					# "LDO_1V2", "P5V0"

					header_labels.append("port")
					header_labels.extend(raillabels)
					header_labels.append("time")

				with open(savefilename, 'w', newline="") as output_file:
					writer = csv.writer(output_file)
					writer.writerow(header_string)
					writer.writerow("")
					writer.writerow(header_info)
					writer.writerow("")
					writer.writerow(header_labels)

			self.display_data()

	def stop_data(self):
		# called when stopData clicked - stops displaying data in lineEdits
		# if the graph is running then it stops graph timer

		global ser, timer, restart, newData, graphing, stopsavingdata, stopsavingwasgraphing, firsttime, startsavingdata

		ser.close()

		restart = True
		newData = False

		if self.startSavingStopping.text() == "Stop Saving Data":
			startsavingdata = False
			stopsavingdata = True
			self.startSavingStopping.setText("Start Saving Data")

		if stopsavingdata == True:
			firsttime = False
			if graphing == True: 
				stopsavingwasgraphing = True

		#if self.displayButton.text() == "Stop Data":
		#	self.displayButton.setText("Display Data")

		try:
			if firsttime == False:
				self.appendRewriteBox.show()
				self.appendRewriteBox.setChecked(True)
		except NameError: pass

		graphing = False

		try: self.timer.stop()
		except AttributeError: pass

	def stop_saving_data(self):
		# called from start_or_stop - stops saving data to csv file
	
		global startsavingdata, stopsavingdata, firsttime, stopsavingwasgraphing, newData, graphing

		startsavingdata = False
		stopsavingdata = True
		firsttime = False
		self.startSavingStopping.setText("Start Saving Data")

		print("Stopping saving data...")

		self.stop_data()

		# if this is not the first time writing to this file, show append checkbox
		if firsttime == False:
			self.appendRewriteBox.show()
			self.appendRewriteBox.setChecked(True)

		# if graph running before stopped saving data, resume graph
		try:
			if stopsavingwasgraphing == True:
				if newData == True:
					graphing = True
		except NameError: pass

	def tab_changed(self):
		# called when tabWidget is changed from New to Saved Data or vice versa

		global newData, infinitelinetimer

		if self.tabWidget.currentIndex() == 0:
			self.new_data_tab_setup()

			# if infiniteline is active, stop when changed to different tab
			try:
				if self.infinitelinetimer.isActive() == True: self.infinitelinetimer.stop()
			except AttributeError: pass

		elif self.tabWidget.currentIndex() == 1:
			# if actively reading data from serial, stop when changed to different tab
			try:
				if newData == True: self.stop_data()
			except NameError: pass
			
			self.saved_data_tab_setup()

	def text_display(self):
		# called in read serial - displays data from plainTextEdit in lineEdits

		text = self.plainTextEdit.toPlainText()
		dataArray = text.split("\n")

		for eachLine in dataArray:
			if len(eachLine) > 1:
				try:
					dataLines = eachLine.split(" ")
					dataLines = list(filter(None, dataLines))

					if porttype == '1':
						self.lineEdit1_1.setText((dataLines[1]))
						self.lineEdit1_2.setText((dataLines[2]))
						self.lineEdit1_3.setText((dataLines[3]))
						self.lineEdit1_4.setText((dataLines[4]))
						self.lineEdit1_5.setText((dataLines[5]))
						self.lineEdit1_6.setText((dataLines[6]))
						self.lineEdit1_7.setText((dataLines[7]))
						self.lineEdit1_8.setText((dataLines[8]))
						self.lineEdit1_9.setText((dataLines[9]))
						self.lineEdit1_10.setText((dataLines[10]))
					if porttype == '2':
						self.lineEdit2_1.setText((dataLines[1]))
						self.lineEdit2_2.setText((dataLines[2]))
						self.lineEdit2_3.setText((dataLines[3]))
						self.lineEdit2_4.setText((dataLines[4]))
						self.lineEdit2_5.setText((dataLines[5]))
						self.lineEdit2_6.setText((dataLines[6]))
						self.lineEdit2_7.setText((dataLines[7]))
						self.lineEdit2_8.setText((dataLines[8]))
						self.lineEdit2_9.setText((dataLines[9]))
					if porttype == '3':
						self.lineEdit3_1.setText((dataLines[1]))
						self.lineEdit3_2.setText((dataLines[2]))
						self.lineEdit3_3.setText((dataLines[3]))
						self.lineEdit3_4.setText((dataLines[4]))
						self.lineEdit3_5.setText((dataLines[5]))
						self.lineEdit3_6.setText((dataLines[6]))
					if porttype == '4':
						self.lineEdit4_1.setText((dataLines[1]))
						self.lineEdit4_2.setText((dataLines[2]))
						self.lineEdit4_3.setText((dataLines[3]))
						self.lineEdit4_4.setText((dataLines[4]))
						self.lineEdit4_5.setText((dataLines[5]))
						self.lineEdit4_6.setText((dataLines[6]))
						self.lineEdit4_7.setText((dataLines[7]))
						self.lineEdit4_8.setText((dataLines[8]))
				except IndexError:
					# occurs when Teensy emits data in a way that GUI cannot comprehend
					# ex: Teensy displaying 4 rails for J3 on QXP instead of 8
					print("index error")
					warningmsg = QtGui.QMessageBox.warning(self, "Error", "There is a formatting issue with " + 
						"your serial device. Reset or unplug your device and try again.",
						QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)
					self.stop_data()					
					break

	def update_graph(self):
		# called from read_serial or check_box_changed - updates the graph according to the box boolean values

		global box1, box2, box3, box4, box5, box6, box7, box8, box9, box10
		global yar1, curve1, yar2, curve2, yar3, curve3, yar4, curve4, yar5, curve5, yar6, curve6
		global yar7, curve7, yar8, curve8, yar9, curve9, yar10, curve10
		global count1, count2, count3, count4, count5, count6, count7, count8, count9, count10
		global timer, restart, graphing

		if newData == True:

			print("Graphing serial data...")
			graphing = True

			self.graphicsView.clear()
			self.timer = QtCore.QTimer()

			# initialize and reset arrays and count variables
			yar1 = [0]*50
			count1 = 50
			yar2 = [0]*50
			count2 = 50
			yar3 = [0]*50
			count3 = 50
			yar4 = [0]*50
			count4 = 50
			yar5 = [0]*50
			count5 = 50
			yar6 = [0]*50
			count6 = 50
			yar7 = [0]*50
			count7 = 50
			yar8 = [0]*50
			count8 = 50
			yar9 = [0]*50
			count9 = 50
			yar10 = [0]*50
			count10 = 50
	
			self.check_boxes_new()
	
			# if box is checked, define curve and call update method for each power rail
			if box1 == True:
				curve1 = self.graphicsView.plotItem.plot(yar1, pen=pyqtgraph.mkPen('r'))
				self.timer.timeout.connect(self.update1)

			if box2 == True:
				curve2 = self.graphicsView.plotItem.plot(yar2, pen=pyqtgraph.mkPen('g'))
				self.timer.timeout.connect(self.update2)
	
			if box3 == True:
				curve3 = self.graphicsView.plotItem.plot(yar3, pen=pyqtgraph.mkPen('b'))
				self.timer.timeout.connect(self.update3)
	
			if box4 == True:
				curve4 = self.graphicsView.plotItem.plot(yar4, pen=pyqtgraph.mkPen('c'))
				self.timer.timeout.connect(self.update4)

			if box5 == True:
				curve5 = self.graphicsView.plotItem.plot(yar5, pen=pyqtgraph.mkPen('m'))
				self.timer.timeout.connect(self.update5)

			if box6 == True:
				curve6 = self.graphicsView.plotItem.plot(yar6, pen=pyqtgraph.mkPen('y'))
				self.timer.timeout.connect(self.update6)

			if box7 == True:
				curve7 = self.graphicsView.plotItem.plot(yar7, pen=pyqtgraph.mkPen(0, 128, 0))
				self.timer.timeout.connect(self.update7)
	
			if box8 == True:
				curve8 = self.graphicsView.plotItem.plot(yar8, pen=pyqtgraph.mkPen(255, 127, 80))
				self.timer.timeout.connect(self.update8)

			if box9 == True:
				curve9 = self.graphicsView.plotItem.plot(yar9, pen=pyqtgraph.mkPen(148, 0, 211))
				self.timer.timeout.connect(self.update9)

			if box10 == True:
				curve10 = self.graphicsView.plotItem.plot(yar10, pen=pyqtgraph.mkPen(165, 42, 42))
				self.timer.timeout.connect(self.update10)

			self.timer.start(10) # update every 10 ms

	def update1(self):
		# called from update_graph - updates graph for box1 if checked

		global yar1, curve1, count1, newData

		# break down plainTextEdit text into a list of each line
		text = self.plainTextEdit.toPlainText()
		dataArray = text.split("\n")

		for eachLine in dataArray:
			if len(eachLine) > 1:
				# remove any empty strings
				dataLines = eachLine.split(" ")
				dataLines = list(filter(None, dataLines))
					
				# remove the oldest data point from the beginning of yar1
				yar1.pop(0)
				# add the newest data point to the end of yar1
				yar1.append(int(dataLines[1]))

		# for each new line of data read, increase count (x-axis) by 1
		if newData == True: count1 += 1

		curve1.setData(yar1)
		curve1.setPos(count1, 0) # shifts plot - creates scrolling x-axis
		QApplication.processEvents()

	def update2(self):
		# called from update_graph - updates graph for box2 if checked

		global yar2, curve2, count2, newData

		# break down plainTextEdit text into a list of each line
		text = self.plainTextEdit.toPlainText()
		dataArray = text.split("\n")

		for eachLine in dataArray:
			if len(eachLine) > 1:
				# remove any empty strings
				dataLines = eachLine.split(" ")
				dataLines = list(filter(None, dataLines))
					
				# remove the oldest data point from the beginning of yar2
				yar2.pop(0)
				# add the newest data point to the end of yar2
				yar2.append(int(dataLines[2]))

		# for each new line of data read, increase count (x-axis) by 1
		if newData == True: count2 += 1

		curve2.setData(yar2)
		curve2.setPos(count2, 0) # shifts plot - creates scrolling x-axis
		QApplication.processEvents()

	def update3(self):
		# called from update_graph - updates graph for box3 if checked

		global yar3, curve3, count3, newData

		# break down plainTextEdit text into a list of each line
		text = self.plainTextEdit.toPlainText()
		dataArray = text.split("\n")

		for eachLine in dataArray:
			if len(eachLine) > 1:
				# remove any empty strings
				dataLines = eachLine.split(" ")
				dataLines = list(filter(None, dataLines))
					
				# remove the oldest data point from the beginning of yar3
				yar3.pop(0)
				# add the newest data point to the end of yar3
				yar3.append(int(dataLines[3]))

		# for each new line of data read, increase count (x-axis) by 1
		if newData == True: count3 += 1

		curve3.setData(yar3)
		curve3.setPos(count3, 0) # shifts plot - creates scrolling x-axis
		QApplication.processEvents()

	def update4(self):
		# called from update_graph - updates graph for box4 if checked

		global yar4, curve4, count4, newData

		# break down plainTextEdit text into a list of each line
		text = self.plainTextEdit.toPlainText()
		dataArray = text.split("\n")

		for eachLine in dataArray:
			if len(eachLine) > 1:
				# remove any empty strings
				dataLines = eachLine.split(" ")
				dataLines = list(filter(None, dataLines))
					
				# remove the oldest data point from the beginning of yar4
				yar4.pop(0)
				# add the newest data point to the end of yar4
				yar4.append(int(dataLines[4]))
		
		# for each new line of data read, increase count (x-axis) by 1
		if newData == True: count4 += 1

		curve4.setData(yar4)
		curve4.setPos(count4, 0) # shifts plot - creates scrolling x-axis
		QApplication.processEvents()

	def update5(self):
		# called from update_graph - updates graph for box5 if checked

		global yar5, curve5, count5, newData

		# break down plainTextEdit text into a list of each line
		text = self.plainTextEdit.toPlainText()
		dataArray = text.split("\n")

		for eachLine in dataArray:
			if len(eachLine) > 1:
				# remove any empty strings
				dataLines = eachLine.split(" ")
				dataLines = list(filter(None, dataLines))
					
				# remove the oldest data point from the beginning of yar5
				yar5.pop(0)
				# add the newest data point to the end of yar5
				yar5.append(int(dataLines[5]))

		# for each new line of data read, increase count (x-axis) by 1
		if newData == True: count5 += 1

		curve5.setData(yar5)
		curve5.setPos(count5, 0) # shifts plot - creates scrolling x-axis
		QApplication.processEvents()

	def update6(self):
		# called from update_graph - updates graph for box6 if checked

		global yar6, curve6, count6, newData

		# break down plainTextEdit text into a list of each line
		text = self.plainTextEdit.toPlainText()
		dataArray = text.split("\n")

		for eachLine in dataArray:
			if len(eachLine) > 1:
				# remove any empty strings
				dataLines = eachLine.split(" ")
				dataLines = list(filter(None, dataLines))
					
				# remove the oldest data point from the beginning of yar6
				yar6.pop(0)
				# add the newest data point to the end of yar6
				yar6.append(int(dataLines[6]))

		# for each new line of data read, increase count (x-axis) by 1
		if newData == True: count6 += 1

		curve6.setData(yar6)
		curve6.setPos(count6, 0) # shifts plot - creates scrolling x-axis
		QApplication.processEvents()

	def update7(self):
		# called from update_graph - updates graph for box7 if checked

		global yar7, curve7, count7, newData

		# break down plainTextEdit text into a list of each line
		text = self.plainTextEdit.toPlainText()
		dataArray = text.split("\n")

		for eachLine in dataArray:
			if len(eachLine) > 1:
				# remove any empty strings
				dataLines = eachLine.split(" ")
				dataLines = list(filter(None, dataLines))
					
				# remove the oldest data point from the beginning of yar7
				yar7.pop(0)
				# add the newest data point to the end of yar7
				yar7.append(int(dataLines[7]))

		# for each new line of data read, increase count (x-axis) by 1
		if newData == True: count7 += 1

		curve7.setData(yar7)
		curve7.setPos(count7, 0) # shifts plot - creates scrolling x-axis
		QApplication.processEvents()

	def update8(self):
		# called from update_graph - updates graph for box8 if checked

		global yar8, curve8, count8, newData

		# break down plainTextEdit text into a list of each line
		text = self.plainTextEdit.toPlainText()
		dataArray = text.split("\n")

		for eachLine in dataArray:
			if len(eachLine) > 1:
				# remove any empty strings
				dataLines = eachLine.split(" ")
				dataLines = list(filter(None, dataLines))
					
				# remove the oldest data point from the beginning of yar8
				yar8.pop(0)
				# add the newest data point to the end of yar8
				yar8.append(int(dataLines[8]))

		# for each new line of data read, increase count (x-axis) by 1
		if newData == True: count8 += 1

		curve8.setData(yar8)
		curve8.setPos(count8, 0) # shifts plot - creates scrolling x-axis
		QApplication.processEvents()

	def update9(self):
		# called from update_graph - updates graph for box9 if checked

		global yar9, curve9, count9, newData

		# break down plainTextEdit text into a list of each line
		text = self.plainTextEdit.toPlainText()
		dataArray = text.split("\n")

		for eachLine in dataArray:
			if len(eachLine) > 1:
				# remove any empty strings
				dataLines = eachLine.split(" ")
				dataLines = list(filter(None, dataLines))
					
				# remove the oldest data point from the beginning of yar9
				yar9.pop(0)
				# add the newest data point to the end of yar9
				yar9.append(int(dataLines[9]))

		# for each new line of data read, increase count (x-axis) by 1
		if newData == True: count9 += 1

		curve9.setData(yar9)
		curve9.setPos(count9, 0) # shifts plot - creates scrolling x-axis
		QApplication.processEvents()

	def update10(self):
		# called from update_graph - updates graph for box10 if checked

		global yar10, curve10, count10, newData

		# break down plainTextEdit text into a list of each line
		text = self.plainTextEdit.toPlainText()
		dataArray = text.split("\n")

		for eachLine in dataArray:
			if len(eachLine) > 1:
				# remove any empty strings
				dataLines = eachLine.split(" ")
				dataLines = list(filter(None, dataLines))
					
				# remove the oldest data point from the beginning of yar10
				yar10.pop(0)
				# add the newest data point to the end of yar10
				yar10.append(int(dataLines[10]))

		# for each new line of data read, increase count (x-axis) by 1
		if newData == True: count10 += 1

		curve10.setData(yar10)
		curve10.setPos(count10, 0) # shifts plot - creates scrolling x-axis
		QApplication.processEvents()

###

	def closeEvent(self, event):
		# forces close of serial port when app is exited
		try:
			self.deleteLater()
		except RuntimeError: pass

def appExec():

	import sys
	app = QtGui.QApplication(sys.argv)
	win = MainWindow()
	win.show()
	app.exec_()

def main():

	import sys
	sys.exit(appExec())
    
if __name__ == "__main__":
	main()
