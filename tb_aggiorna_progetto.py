# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:		tb_aggiorna_progetto.py
# Author:	  Tarquini E.
# Created:	 24-09-2018
# -------------------------------------------------------------------------------

import datetime
import os
import shutil
import sqlite3
import sys
import webbrowser
import zipfile


from qgis.core import *
from qgis.gui import *
from qgis.PyQt import uic
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.utils import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'tb_aggiorna_progetto.ui'))


class aggiorna_progetto(QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super(aggiorna_progetto, self).__init__(parent)
        self.setupUi(self)
        self.plugin_dir = os.path.dirname(__file__)

    def aggiorna(self, dir2, dir_output, nome):
        self.show()
        result = self.exec_()
        if result:
            QgsProject.instance().clear()
            for c in iface.activeComposers():
                iface.deleteComposer(c)
            try:
                vers_data_1 = self.plugin_dir + os.sep + "version.txt"
                new_vers = open(vers_data_1, 'r').read()
                vers_data_2 = dir2 + os.sep + "progetto" + os.sep + "version.txt"
                proj_vers = open(vers_data_2, 'r').read()
                pacchetto = self.plugin_dir + os.sep + "data" + os.sep + "progetto_CLE.zip"

                if proj_vers < '0.3' and new_vers == '0.3':
                    pass

            except Exception as z:
                QMessageBox.critical(
                    None, 'ERROR!', 'Error:\n"' + str(z) + '"')
