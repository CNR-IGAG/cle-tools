# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:		cle_cl_ae.py
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


def cl_ae(dialog, layer, feature):
	data_ae = dialog.findChild(QDateEdit,"data_ae")
	today = QDate.currentDate()
	data_ae.setDate(today)
	ID_area = dialog.findChild(QLineEdit,"ID_area")
	ID_infra_a = dialog.findChild(QLineEdit,"ID_infra_a")
	ID_infra_b = dialog.findChild(QLineEdit,"ID_infra_b")
	ID_infra_c = dialog.findChild(QLineEdit,"ID_infra_c")
	ID_infra_d = dialog.findChild(QLineEdit,"ID_infra_d")
	denom = dialog.findChild(QLineEdit,"denom")
	anno_piano = dialog.findChild(QLineEdit,"anno_piano")
	n_aggreg = dialog.findChild(QLineEdit,"n_aggreg")
	n_manuf = dialog.findChild(QLineEdit,"n_manuf")
	superf = dialog.findChild(QLineEdit,"superf")
	rett_max = dialog.findChild(QLineEdit,"rett_max")
	rett_min = dialog.findChild(QLineEdit,"rett_min")
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
	ID_area.editingFinished.connect(lambda: zero_digit(ID_area,10))
	ID_area.textChanged.connect(lambda: disableButton(dialog))
	ID_infra_a.editingFinished.connect(lambda: zero_digit(ID_infra_a,10))
	ID_infra_b.editingFinished.connect(lambda: zero_digit(ID_infra_b,10))
	ID_infra_c.editingFinished.connect(lambda: zero_digit(ID_infra_c,10))
	ID_infra_d.editingFinished.connect(lambda: zero_digit(ID_infra_d,10))
	anno_piano.textEdited.connect(lambda: update_valore(anno_piano))
	n_aggreg.textEdited.connect(lambda: update_valore(n_aggreg))
	n_manuf.textEdited.connect(lambda: update_valore(n_manuf))
	superf.textEdited.connect(lambda: update_valore(superf))
	rett_max.textEdited.connect(lambda: update_valore(rett_max))
	rett_min.textEdited.connect(lambda: update_valore(rett_min))
	rett_max.editingFinished.connect(lambda: alert_area(dialog))
	rett_min.editingFinished.connect(lambda: alert_area(dialog))
	superf.editingFinished.connect(lambda: alert_area_2(dialog))
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

def alert_area(dialog):
	rett_max = dialog.findChild(QLineEdit,"rett_max")
	rett_min = dialog.findChild(QLineEdit,"rett_min")
	if (rett_max.text() != '') and (rett_min.text() != ''):
		if int(rett_min.text()) > int(rett_max.text()):
			QMessageBox.warning(None, u'WARNING!', u"The value of the '15 MINIMA' field is greater than the value of the '14 MASSIMA' field!")
			rett_min.setText('')
			rett_max.setText('')

def alert_area_2(dialog):
	rett_max = dialog.findChild(QLineEdit,"rett_max")
	rett_min = dialog.findChild(QLineEdit,"rett_min")
	superf = dialog.findChild(QLineEdit,"superf")
	if (rett_max.text() != '') and (rett_min.text() != '') and (superf.text() != ''):
		if int(superf.text()) < int(rett_max.text())*int(rett_min.text()):
			QMessageBox.warning(None, u'WARNING!', u"The product of '14 MASSIMA' field for '15 MINIMA' field is higher than the value of the '13 SUPERFICIE DELL''AREA' field!")
			rett_min.setText('')
			rett_max.setText('')
			superf.setText('')

def disableButton(dialog):
	ID_area = dialog.findChild(QLineEdit,"ID_area")
	button_box = dialog.findChild(QDialogButtonBox, "button_box")

	if len(ID_area.text()) > 1:
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