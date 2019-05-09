# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:		cle_cl_us.py
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


def cl_us(dialog, layer, feature):
	data_us = dialog.findChild(QDateEdit,"data_us")
	today = QDate.currentDate()
	data_us.setDate(today)
	sezione = dialog.findChild(QLineEdit,"sezione")
	ID_aggr = dialog.findChild(QLineEdit,"ID_aggr")
	ID_unit = dialog.findChild(QLineEdit,"ID_unit")
	ID_area = dialog.findChild(QLineEdit,"ID_area")
	ID_infra_a = dialog.findChild(QLineEdit,"ID_infra_a")
	ID_infra_b = dialog.findChild(QLineEdit,"ID_infra_b")
	ID_infra_c = dialog.findChild(QLineEdit,"ID_infra_c")
	ID_infra_d = dialog.findChild(QLineEdit,"ID_infra_d")
	civico = dialog.findChild(QLineEdit,"civico")
	n_piani = dialog.findChild(QLineEdit,"n_piani")
	alt_totale = dialog.findChild(QLineEdit,"alt_totale")
	superf_m = dialog.findChild(QLineEdit,"superf_m")
	zona_ms = dialog.findChild(QComboBox,"zona_ms")
	inst_name = dialog.findChild(QLabel,"inst_name")
	inst_fran = dialog.findChild(QCheckBox,"inst_fran")
	inst_liq = dialog.findChild(QCheckBox,"inst_liq")
	inst_fag = dialog.findChild(QCheckBox,"inst_fag")
	inst_ced = dialog.findChild(QCheckBox,"inst_ced")
	inst_cav = dialog.findChild(QCheckBox,"inst_cav")
	isolato = dialog.findChild(QComboBox,"isolato")
	posizio = dialog.findChild(QComboBox,"posizio")
	spec = dialog.findChild(QComboBox,"spec")
	specialis = dialog.findChild(QComboBox,"specialis")
	strutt_ver = dialog.findChild(QComboBox,"strutt_ver")
	tipo_mur = dialog.findChild(QComboBox,"tipo_mur")
	uso_a = dialog.findChild(QCheckBox,"uso_a")
	uso_a_1 = dialog.findChild(QLineEdit, "uso_a_1")
	uso_b = dialog.findChild(QCheckBox,"uso_b")
	uso_b_1 = dialog.findChild(QLineEdit, "uso_b_1")
	uso_c = dialog.findChild(QCheckBox,"uso_c")
	uso_c_1 = dialog.findChild(QLineEdit, "uso_c_1")
	uso_d = dialog.findChild(QCheckBox,"uso_d")
	uso_d_1 = dialog.findChild(QLineEdit, "uso_d_1")
	uso_e = dialog.findChild(QCheckBox,"uso_e")
	uso_e_1 = dialog.findChild(QLineEdit, "uso_e_1")
	uso_f = dialog.findChild(QCheckBox,"uso_f")
	uso_f_1 = dialog.findChild(QLineEdit, "uso_f_1")
	uso_g = dialog.findChild(QCheckBox,"uso_g")
	uso_g_1 = dialog.findChild(QLineEdit, "uso_g_1")
	occupanti = dialog.findChild(QLineEdit, "occupanti")
	localita = dialog.findChild(QComboBox,"localita")
	cod_local = dialog.findChild(QLineEdit,"cod_local")

	posizio.setEnabled(False)
	specialis.setEnabled(False)
	tipo_mur.setEnabled(False)

	inst_name.hide()
	inst_fran.hide()
	inst_liq.hide()
	inst_fag.hide()
	inst_ced.hide()
	inst_cav.hide()

	uso_a.setEnabled(False)
	uso_a_1.setEnabled(False)
	uso_b.setEnabled(False)
	uso_b_1.setEnabled(False)
	uso_c.setEnabled(False)
	uso_c_1.setEnabled(False)
	uso_d.setEnabled(False)
	uso_d_1.setEnabled(False)
	uso_e.setEnabled(False)
	uso_e_1.setEnabled(False)
	uso_f.setEnabled(False)
	uso_f_1.setEnabled(False)
	uso_g.setEnabled(False)
	uso_g_1.setEnabled(False)

	button_box = dialog.findChild(QDialogButtonBox, "button_box")
	button_box.setEnabled(False)
	help_button = dialog.findChild(QPushButton, "help_button")
	help_button.clicked.connect(lambda: webbrowser.open('https://www.youtube.com/watch?v=drs3COLtML8'))

	localita.currentIndexChanged.connect(lambda: update_localita(dialog, cod_local, localita))
	sezione.textEdited.connect(lambda: update_valore(sezione))
	ID_aggr.editingFinished.connect(lambda: zero_digit(ID_aggr, 10, 1))
	ID_unit.editingFinished.connect(lambda: zero_digit(ID_unit, 3, 0))
	ID_area.editingFinished.connect(lambda: zero_digit(ID_area,10, 0))
	ID_infra_a.editingFinished.connect(lambda: zero_digit(ID_infra_a,10, 0))
	ID_infra_b.editingFinished.connect(lambda: zero_digit(ID_infra_b,10, 0))
	ID_infra_c.editingFinished.connect(lambda: zero_digit(ID_infra_c,10, 0))
	ID_infra_d.editingFinished.connect(lambda: zero_digit(ID_infra_d,10, 0))
	civico.textEdited.connect(lambda: update_valore(civico))
	n_piani.textEdited.connect(lambda: update_valore(n_piani))
	alt_totale.textEdited.connect(lambda: update_valore(alt_totale))
	superf_m.textEdited.connect(lambda: update_valore(superf_m))
	ID_unit.textChanged.connect(lambda: disableButton(dialog))
	ID_aggr.textChanged.connect(lambda: disableButton(dialog))
	isolato.currentIndexChanged.connect(lambda: disablePosizio(dialog))
	spec.currentIndexChanged.connect(lambda: disableSpecialis(dialog))
	strutt_ver.currentIndexChanged.connect(lambda: disableTipo_mur(dialog))
	zona_ms.currentIndexChanged.connect(lambda: disableInstab(dialog))
	occupanti.textEdited.connect(lambda: update_valore(occupanti))
	uso_a.stateChanged.connect(lambda: check_button_1(dialog))
	uso_b.stateChanged.connect(lambda: check_button_2(dialog))
	uso_c.stateChanged.connect(lambda: check_button_3(dialog))
	uso_d.stateChanged.connect(lambda: check_button_4(dialog))
	uso_e.stateChanged.connect(lambda: check_button_5(dialog))
	uso_f.stateChanged.connect(lambda: check_button_6(dialog))
	uso_g.stateChanged.connect(lambda: check_button_7(dialog))

def zero_digit(campo,n,m):
	a = len(campo.text())

	if a < n:
		b = n - a
		if m == 0:
			c = ('0'*b) + campo.text()
		elif m == 1:
			c = ('0'*b) + campo.text() + '00'
		campo.setText(c)
	elif a > n:
		return campo.setText("")

def update_valore(value):
	value.setText(re.sub('[^0-9]','', value.text()))

def check_button_1(dialog):
	uso_a = dialog.findChild(QCheckBox,"uso_a")
	uso_a_1 = dialog.findChild(QLineEdit, "uso_a_1")
	if uso_a.isChecked() == True:
		uso_a_1.setEnabled(True)
	else:
		uso_a_1.setText("")
		uso_a_1.setEnabled(False)

def check_button_2(dialog):
	uso_b = dialog.findChild(QCheckBox,"uso_b")
	uso_b_1 = dialog.findChild(QLineEdit, "uso_b_1")
	if uso_b.isChecked() == True:
		uso_b_1.setEnabled(True)
	else:
		uso_b_1.setText("")
		uso_b_1.setEnabled(False)

def check_button_3(dialog):
	uso_c = dialog.findChild(QCheckBox,"uso_c")
	uso_c_1 = dialog.findChild(QLineEdit, "uso_c_1")
	if uso_c.isChecked() == True:
		uso_c_1.setEnabled(True)
	else:
		uso_c_1.setText("")
		uso_c_1.setEnabled(False)

def check_button_4(dialog):
	uso_d = dialog.findChild(QCheckBox,"uso_d")
	uso_d_1 = dialog.findChild(QLineEdit, "uso_d_1")
	if uso_d.isChecked() == True:
		uso_d_1.setEnabled(True)
	else:
		uso_d_1.setText("")
		uso_d_1.setEnabled(False)

def check_button_5(dialog):
	uso_e = dialog.findChild(QCheckBox,"uso_e")
	uso_e_1 = dialog.findChild(QLineEdit, "uso_e_1")
	if uso_e.isChecked() == True:
		uso_e_1.setEnabled(True)
	else:
		uso_e_1.setText("")
		uso_e_1.setEnabled(False)

def check_button_6(dialog):
	uso_f = dialog.findChild(QCheckBox,"uso_f")
	uso_f_1 = dialog.findChild(QLineEdit, "uso_f_1")
	if uso_f.isChecked() == True:
		uso_f_1.setEnabled(True)
	else:
		uso_f_1.setText("")
		uso_f_1.setEnabled(False)

def check_button_7(dialog):
	uso_g = dialog.findChild(QCheckBox,"uso_g")
	uso_g_1 = dialog.findChild(QLineEdit, "uso_g_1")
	if uso_g.isChecked() == True:
		uso_g_1.setEnabled(True)
	else:
		uso_g_1.setText("")
		uso_g_1.setEnabled(False)

def disableButton(dialog):
	ID_aggr = dialog.findChild(QLineEdit,"ID_aggr")
	ID_unit = dialog.findChild(QLineEdit,"ID_unit")
	button_box = dialog.findChild(QDialogButtonBox, "button_box")
	check_campi = [ID_aggr.text(), ID_unit.text()]
	check_value = []

	for x in check_campi:
		if len(x) > 1:
			value_campi = 1
			check_value.append(value_campi)
		else:
			value_campi = 0
			check_value.append(value_campi)
	campi = sum(check_value)

	if campi > 1:
		button_box.setEnabled(True)
	else:
		button_box.setEnabled(False)

def disablePosizio(dialog):
	isolato = dialog.findChild(QComboBox,"isolato")
	posizio = dialog.findChild(QComboBox,"posizio")
	if isolato.currentText() == "NO":
		posizio.setEnabled(True)
	if isolato.currentText() == "SI":
		posizio.setCurrentIndex(0)
		posizio.setEnabled(False)

def disableSpecialis(dialog):
	spec = dialog.findChild(QComboBox,"spec")
	specialis = dialog.findChild(QComboBox,"specialis")
	if spec.currentText() == "SI":
		specialis.setEnabled(True)
	if spec.currentText() == "NO":
		specialis.setCurrentIndex(0)
		specialis.setEnabled(False)

def disableTipo_mur(dialog):
	strutt_ver = dialog.findChild(QComboBox,"strutt_ver")
	tipo_mur = dialog.findChild(QComboBox,"tipo_mur")
	if strutt_ver.currentText() in ("4 - Muratura","5 - Mista (muratura/c.a.)"):
		tipo_mur.setEnabled(True)
	else:
		tipo_mur.setCurrentIndex(0)
		tipo_mur.setEnabled(False)

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