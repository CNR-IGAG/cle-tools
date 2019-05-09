# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:		cle_cl_ac.py
# Author:	  Tarquini E.
# Created:	 22-09-2018
#-------------------------------------------------------------------------------

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import *
from qgis.gui import *
from qgis.core import *
from qgis.PyQt.QtWidgets import *
import webbrowser, re


def cl_ac(dialog, layer, feature):
	ID_infra = dialog.findChild(QLineEdit,"ID_infra")
	data_ac = dialog.findChild(QDateEdit,"data_ac")
	today = QDate.currentDate()
	data_ac.setDate(today)
	largh_max = dialog.findChild(QLineEdit,"largh_max")
	largh_min = dialog.findChild(QLineEdit,"largh_min")
	lungh = dialog.findChild(QLineEdit,"lungh")
	lungh_vuo = dialog.findChild(QLineEdit,"lungh_vuo")
	n_aggreg = dialog.findChild(QLineEdit,"n_aggreg")
	n_manuf = dialog.findChild(QLineEdit,"n_manuf")
	el_ferrov = dialog.findChild(QLineEdit,"el_ferrov")
	el_pont = dialog.findChild(QLineEdit,"el_pont")
	el_tunn = dialog.findChild(QLineEdit,"el_tunn")
	el_pont_at = dialog.findChild(QLineEdit,"el_pont_at")
	el_muri = dialog.findChild(QLineEdit,"el_muri")
	pendenza = dialog.findChild(QLineEdit,"pendenza")
	zona_ms = dialog.findChild(QComboBox,"zona_ms")
	inst_name = dialog.findChild(QLabel,"inst_name")
	inst_fran = dialog.findChild(QCheckBox,"inst_fran")
	inst_liq = dialog.findChild(QCheckBox,"inst_liq")
	inst_fag = dialog.findChild(QCheckBox,"inst_fag")
	inst_ced = dialog.findChild(QCheckBox,"inst_ced")
	inst_cav = dialog.findChild(QCheckBox,"inst_cav")
	localita = dialog.findChild(QComboBox,"localita")
	cod_local = dialog.findChild(QLineEdit,"cod_local")

	inst_name.hide()
	inst_fran.hide()
	inst_liq.hide()
	inst_fag.hide()
	inst_ced.hide()
	inst_cav.hide()

	button_box = dialog.findChild(QDialogButtonBox, "button_box")
	button_box.setEnabled(False)
	help_button = dialog.findChild(QPushButton, "help_button")
	help_button.clicked.connect(lambda: webbrowser.open('https://www.youtube.com/watch?v=drs3COLtML8'))

	localita.currentIndexChanged.connect(lambda: update_localita(dialog, cod_local, localita))
	ID_infra.editingFinished.connect(lambda: zero_digit(ID_infra, 10))
	ID_infra.textChanged.connect(lambda: disableButton(dialog))
	largh_max.textEdited.connect(lambda: update_valore(largh_max))
	largh_min.textEdited.connect(lambda: update_valore(largh_min))
	lungh.textEdited.connect(lambda: update_valore(lungh))
	lungh_vuo.textEdited.connect(lambda: update_valore(lungh_vuo))
	n_aggreg.textEdited.connect(lambda: update_valore(n_aggreg))
	n_manuf.textEdited.connect(lambda: update_valore(n_manuf))
	el_ferrov.textEdited.connect(lambda: update_valore(el_ferrov))
	el_pont.textEdited.connect(lambda: update_valore(el_pont))
	el_tunn.textEdited.connect(lambda: update_valore(el_tunn))
	el_pont_at.textEdited.connect(lambda: update_valore(el_pont_at))
	el_muri.textEdited.connect(lambda: update_valore(el_muri))
	pendenza.textEdited.connect(lambda: update_valore(pendenza))
	largh_max.editingFinished.connect(lambda: alert_larg(dialog))
	largh_min.editingFinished.connect(lambda: alert_larg(dialog))
	lungh.editingFinished.connect(lambda: alert_larg_2(dialog))
	lungh_vuo.editingFinished.connect(lambda: alert_larg_2(dialog))
	zona_ms.currentIndexChanged.connect(lambda: disableInstab(dialog))

def zero_digit(campo,n):
	a = len(campo.text())

	if a < n:
		b = n - a
		c = ('0'*b) + campo.text()
		campo.setText(c)
	elif a > n:
		return campo.setText("")

def update_valore(value):
	value.setText(re.sub('[^0-9]','', value.text()))

def alert_larg(dialog):
	largh_max = dialog.findChild(QLineEdit,"largh_max")
	largh_min = dialog.findChild(QLineEdit,"largh_min")
	if (largh_max.text() != '') and (largh_min.text() != ''):
		if int(largh_min.text()) > int(largh_max.text()):
			QMessageBox.warning(None, u'WARNING!', u"The value of the '15 MINIMA' field is greater than the value of the '14 MASSIMA' field!")
			largh_min.setText('')
			largh_max.setText('')

def alert_larg_2(dialog):
	lungh = dialog.findChild(QLineEdit,"lungh")
	lungh_vuo = dialog.findChild(QLineEdit,"lungh_vuo")
	if (lungh.text() != '') and (lungh_vuo.text() != ''):
		if int(lungh_vuo.text()) > int(lungh.text()):
			QMessageBox.warning(None, u'WARNING!', u"The value of the '17 LUNGHEZZA TRATTO STRADALE SENZA AGGREGATIE UNITA' ISOLATE INTERFERENTI' field is greater than the value of the '16 LUNGHEZZA COMPLESSIVA' field!")
			lungh_vuo.setText('')
			lungh.setText('')

def disableButton(dialog):
	ID_infra = dialog.findChild(QLineEdit,"ID_infra")
	button_box = dialog.findChild(QDialogButtonBox, "button_box")

	if len(ID_infra.text()) > 1:
		button_box.setEnabled(True)
	else:
		button_box.setEnabled(False)

def disableInstab(dialog):
	zona_ms = dialog.findChild(QComboBox,"zona_ms")
	inst_name = dialog.findChild(QLabel,"inst_name")
	inst_fran = dialog.findChild(QCheckBox,"inst_fran")
	inst_liq = dialog.findChild(QCheckBox,"inst_liq")
	inst_fag = dialog.findChild(QCheckBox,"inst_fag")
	inst_ced = dialog.findChild(QCheckBox,"inst_ced")
	inst_cav = dialog.findChild(QCheckBox,"inst_cav")
	if zona_ms.currentText() == "3 - Instabile":
		inst_name.show()
		inst_fran.show()
		inst_liq.show()
		inst_fag.show()
		inst_ced.show()
		inst_cav.show()
		inst_fran.setEnabled(True)
		inst_liq.setEnabled(True)
		inst_fag.setEnabled(True)
		inst_ced.setEnabled(True)
		inst_cav.setEnabled(True)
	else:
		inst_fran.setChecked(False)
		inst_fran.setEnabled(False)
		inst_liq.setChecked(False)
		inst_liq.setEnabled(False)
		inst_fag.setChecked(False)
		inst_fag.setEnabled(False)
		inst_ced.setChecked(False)
		inst_ced.setEnabled(False)
		inst_cav.setChecked(False)
		inst_cav.setEnabled(False)

def update_localita(dialog, cod_local, localita):
	localita = dialog.findChild(QComboBox,"localita")
	cod_local = dialog.findChild(QLineEdit,"cod_local")
	TipoIndagine = str(localita.currentText().strip()).split("  -  ")[1]
	cod_local.setText(TipoIndagine)