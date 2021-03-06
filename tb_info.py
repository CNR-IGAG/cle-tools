# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:		tb_info.py
# Author:	  Tarquini E.
# Created:	 08-02-2018
# -------------------------------------------------------------------------------

import os
import subprocess
import sys
import webbrowser

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), "tb_info.ui"))


class info(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(info, self).__init__(parent)
        self.setupUi(self)
        self.plugin_dir = os.path.dirname(__file__)

    def help(self):
        self.pushButton_ita.clicked.connect(
            # lambda: self.open_pdf(os.path.join(self.plugin_dir, "manuale.pdf"))
            lambda: webbrowser.open("https://cle-tools.readthedocs.io")
        )
        # self.pushButton_eng.clicked.connect(lambda: self.open_pdf(self.plugin_dir + os.sep + "manual.pdf"))
        self.pushButton_www.clicked.connect(
            lambda: webbrowser.open("https://github.com/CNR-IGAG/cle-tools")
        )

        self.show()

    def open_pdf(self, pdf_path):
        if sys.platform == "win32":
            os.startfile(pdf_path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, pdf_path])
