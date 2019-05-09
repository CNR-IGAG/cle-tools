# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:		tb_report_cle.py
# Author:	  Tarquini E.
# Created:	 20-11-2018
#-------------------------------------------------------------------------------

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import *
from qgis.core import *
from qgis.gui import *
import os, sys, webbrowser, constants

FORM_CLASS, _ = uic.loadUiType(os.path.join(
	os.path.dirname(__file__), 'tb_report_cle.ui'))


class report_cle(QtGui.QDialog, FORM_CLASS):

	def __init__(self, parent=None):
		"""Constructor."""
		self.iface = iface
		super(report_cle, self).__init__(parent)
		self.setupUi(self)
		self.plugin_dir = os.path.dirname(__file__)

	def report(self):
		self.help_button.clicked.connect(lambda: webbrowser.open('https://github.com/CNR-IGAG/mzs-tools/wiki/MzS-Tools'))
		self.disableButton()
		self.show()

	def disableButton(self):
		conteggio = 0

		layers = self.iface.legendInterface().layers()
		for layer in layers:
			if layer.name() in constants.LISTA_LAYER:
				conteggio += 1

		if conteggio > 23:
			self.button_box.setEnabled(True)
			self.alert_text.hide()
		else:
			self.button_box.setEnabled(False)
			self.alert_text.show()