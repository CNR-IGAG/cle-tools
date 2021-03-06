# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:		tb_esporta_shp.py
# Author:	  Tarquini E.
# Created:	 08-02-2018
# -------------------------------------------------------------------------------
import os
import shutil
import sqlite3
import sys
import webbrowser
import zipfile

from qgis.core import *
from qgis.core import QgsMessageLog
from qgis.gui import *
from qgis.PyQt import uic
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.utils import *

from . import constants
from .setup_workers import setup_workers
from .workers.export_worker import ExportWorker

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'tb_esporta_shp.ui'))


class esporta_shp(QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        self.iface = iface
        super(esporta_shp, self).__init__(parent)
        self.setupUi(self)
        self.plugin_dir = os.path.dirname(__file__)

    def esporta_prog(self):
        self.help_button.clicked.connect(lambda: webbrowser.open("https://cle-tools.readthedocs.io"))
        self.dir_output.clear()
        self.alert_text.hide()
        self.button_box.setEnabled(False)
        self.dir_output.textChanged.connect(self.disableButton)

        self.show()
        result = self.exec_()
        if result:

            try:
                in_dir = QgsProject.instance().readPath("./")
                out_dir = self.dir_output.text()
                if os.path.exists(out_dir):

                    # create export worker
                    worker = ExportWorker(in_dir, out_dir, self.plugin_dir)

                    # create export log file
                    logfile_path = in_dir + os.sep + "allegati" + os.sep + "log" + os.sep + \
                        str(time.strftime("%Y-%m-%d_%H-%M-%S",
                                          time.gmtime())) + "_export_log.txt"
                    log_file = open(logfile_path, 'a')
                    log_file.write("EXPORT REPORT:" + "\n---------------\n\n")

                    # start export worker
                    setup_workers().start_worker(worker, self.iface,
                                                 'Starting export task...', log_file, logfile_path)

                else:
                    QMessageBox.warning(
                        None, self.tr('WARNING!'), self.tr("The selected directory does not exist!"))

            except Exception as z:
                QMessageBox.critical(
                    None, 'ERROR!', 'Error:\n"' + str(z) + '"')

    def disableButton(self):
        conteggio = 0
        check_campi = [self.dir_output.text()]
        check_value = []

        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            if layer.name() in constants.LISTA_LAYER:
                conteggio += 1

        for x in check_campi:
            if len(x) > 0:
                value_campi = 1
                check_value.append(value_campi)
            else:
                value_campi = 0
                check_value.append(value_campi)
        campi = sum(check_value)

        if conteggio > 5 and campi > 0:
            self.button_box.setEnabled(True)
            self.alert_text.hide()
        elif conteggio > 5 and campi == 0:
            self.button_box.setEnabled(False)
            self.alert_text.hide()
        else:
            self.button_box.setEnabled(False)
            self.alert_text.show()

    def tr(self, message):
        return QCoreApplication.translate('esporta_shp', message)
