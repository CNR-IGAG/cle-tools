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
        super().__init__(parent)
        self.setupUi(self)
        self.plugin_dir = os.path.dirname(__file__)

    def aggiorna(self, dir2, dir_output, nome, proj_vers, new_proj_vers):
        self.show()
        result = self.exec_()
        if result:
            try:
                pacchetto = os.path.join(
                    self.plugin_dir, "data", "progetto_CLE.zip")

                if proj_vers < new_proj_vers:

                    name_output = nome + "_backup_v" + proj_vers + "_" + \
                        datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
                    shutil.copytree(dir2, os.path.join(
                        dir_output, name_output))

                    zip_ref = zipfile.ZipFile(pacchetto, 'r')
                    zip_ref.extractall(dir2)
                    zip_ref.close()

                    shutil.rmtree(os.path.join(dir2, "progetto", "maschere"))
                    shutil.copytree(os.path.join(dir2, "progetto_CLE", "progetto", "maschere"), os.path.join(
                        dir2, "progetto", "maschere"))
                    shutil.rmtree(os.path.join(dir2, "progetto", "script"))
                    shutil.copytree(os.path.join(dir2, "progetto_CLE", "progetto", "script"), os.path.join(
                        dir2, "progetto", "script"))
                    os.remove(os.path.join(dir2, "progetto", "version.txt"))
                    shutil.copyfile(os.path.join(os.path.dirname(__file__), 'version.txt'), os.path.join(
                        dir2, "progetto", "version.txt"))
                    os.remove(os.path.join(dir2, "progetto_CLE.qgs"))
                    shutil.copyfile(os.path.join(
                        dir2, "progetto_CLE", "progetto_CLE.qgs"), os.path.join(dir2, "progetto_CLE.qgs"))

                    shutil.rmtree(os.path.join(dir2, "progetto_CLE"))
                    QMessageBox.information(
                        None, 'INFORMATION!', "The project structure has been updated!\nThe backup copy has been saved in the following directory: " + name_output)

                    QgsProject.instance().read(QgsProject.instance().fileName())

            except Exception as z:
                QMessageBox.critical(
                    None, 'ERROR!', 'Error:\n"' + str(z) + '"')
