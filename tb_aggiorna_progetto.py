# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:		tb_aggiorna_progetto.py
# Author:	  Tarquini E.
# Created:	 24-09-2018
#-------------------------------------------------------------------------------

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import *
from qgis.core import *
from qgis.gui import *
import os, sys, webbrowser, shutil, sqlite3, zipfile, datetime


FORM_CLASS, _ = uic.loadUiType(os.path.join(
	os.path.dirname(__file__), 'tb_aggiorna_progetto.ui'))


class aggiorna_progetto(QtGui.QDialog, FORM_CLASS):

	def __init__(self, parent=None):
		"""Constructor."""
		super(aggiorna_progetto, self).__init__(parent)
		self.setupUi(self)
		self.plugin_dir = os.path.dirname(__file__)

	def aggiorna(self,dir2,dir_output,nome):
		self.show()
		result = self.exec_()
		if result:
			QgsProject.instance().clear()
			for c in iface.activeComposers():
				iface.deleteComposer(c)
			try:
				vers_data_1 = self.plugin_dir + os.sep + "version.txt"
				new_vers = open(vers_data_1,'r').read()
				vers_data_2 = dir2 + os.sep + "progetto" + os.sep + "version.txt"
				proj_vers = open(vers_data_2,'r').read()
				pacchetto = self.plugin_dir + os.sep + "data" + os.sep + "progetto_CLE.zip"

				if proj_vers < '0.2' and new_vers == '0.2':
					pass

			except Exception as z:
				QMessageBox.critical(None, u'ERROR!', u'Error:\n"' + str(z) + '"')
