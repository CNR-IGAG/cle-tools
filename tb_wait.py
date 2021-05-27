# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:		tb_wait.py
# Author:	  Tarquini E.
# Created:	 27-09-2018
# -------------------------------------------------------------------------------

import os
from qgis.PyQt import QtWidgets, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'tb_wait.ui'))


class wait(QtWidgets.QDialog, FORM_CLASS):
    
    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)
        self.setupUi(self)
