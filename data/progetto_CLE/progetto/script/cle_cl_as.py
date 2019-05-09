# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:		cle_cl_as.py
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


def cl_as(dialog, layer, feature):
	data_as = dialog.findChild(QDateEdit,"data_as")
	today = QDate.currentDate()
	data_as.setDate(today)
	sezione = dialog.findChild(QLineEdit,"sezione")
	ID_aggr = dialog.findChild(QLineEdit,"ID_aggr")
	ID_area = dialog.findChild(QLineEdit,"ID_area")
	ID_infra_a = dialog.findChild(QLineEdit,"ID_infra_a")
	ID_infra_b = dialog.findChild(QLineEdit,"ID_infra_b")
	ID_infra_c = dialog.findChild(QLineEdit,"ID_infra_c")
	ID_infra_d = dialog.findChild(QLineEdit,"ID_infra_d")
	n_unita = dialog.findChild(QLineEdit,"n_unita")
	n_edif = dialog.findChild(QLineEdit,"n_edif")
	n_edif_gl = dialog.findChild(QLineEdit,"n_edif_gl")
	n_murat = dialog.findChild(QLineEdit,"n_murat")
	n_ca = dialog.findChild(QLineEdit,"n_ca")
	n_altre = dialog.findChild(QLineEdit,"n_altre")
	altezza = dialog.findChild(QLineEdit,"altezza")
	superf = dialog.findChild(QLineEdit,"superf")
	piani_min = dialog.findChild(QLineEdit,"piani_min")
	piani_max = dialog.findChild(QLineEdit,"piani_max")
	lungh_fron = dialog.findChild(QLineEdit,"lungh_fron")
	us_interf = dialog.findChild(QLineEdit,"us_interf")
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
	sezione.textEdited.connect(lambda: update_valore(sezione))
	ID_aggr.editingFinished.connect(lambda: zero_digit(ID_aggr, 10, 1))
	ID_aggr.textChanged.connect(lambda: disableButton(dialog))
	ID_area.editingFinished.connect(lambda: zero_digit(ID_area,10, 0))
	ID_infra_a.editingFinished.connect(lambda: zero_digit(ID_infra_a,10, 0))
	ID_infra_b.editingFinished.connect(lambda: zero_digit(ID_infra_b,10, 0))
	ID_infra_c.editingFinished.connect(lambda: zero_digit(ID_infra_c,10, 0))
	ID_infra_d.editingFinished.connect(lambda: zero_digit(ID_infra_d,10, 0))
	n_unita.textEdited.connect(lambda: update_valore(n_unita))
	n_edif.textEdited.connect(lambda: update_valore(n_edif))
	n_edif_gl.textEdited.connect(lambda: update_valore(n_edif_gl))
	n_murat.textEdited.connect(lambda: update_valore(n_murat))
	n_ca.textEdited.connect(lambda: update_valore(n_ca))
	n_altre.textEdited.connect(lambda: update_valore(n_altre))
	altezza.textEdited.connect(lambda: update_valore(altezza))
	superf.textEdited.connect(lambda: update_valore(superf))
	piani_min.textEdited.connect(lambda: update_valore(piani_min))
	piani_max.textEdited.connect(lambda: update_valore(piani_max))
	lungh_fron.textEdited.connect(lambda: update_valore(lungh_fron))
	us_interf.textEdited.connect(lambda: update_valore(us_interf))
	n_unita.editingFinished.connect(lambda: alert_us_1(dialog))
	n_edif.editingFinished.connect(lambda: alert_us_1(dialog))
	n_edif_gl.editingFinished.connect(lambda: alert_us_1(dialog))
	n_unita.editingFinished.connect(lambda: alert_us_2(dialog))
	n_murat.editingFinished.connect(lambda: alert_us_2(dialog))
	n_ca.editingFinished.connect(lambda: alert_us_2(dialog))
	n_altre.editingFinished.connect(lambda: alert_us_2(dialog))
	piani_min.editingFinished.connect(lambda: alert_us_3(dialog))
	piani_max.editingFinished.connect(lambda: alert_us_3(dialog))
	zona_ms.currentIndexChanged.connect(lambda: disableInstab(dialog))

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

def alert_us_1(dialog):
	n_unita = dialog.findChild(QLineEdit,"n_unita")
	n_edif = dialog.findChild(QLineEdit,"n_edif")
	n_edif_gl = dialog.findChild(QLineEdit,"n_edif_gl")
	if (n_unita.text() != '') and (n_edif.text() != ''):
		if int(n_edif.text()) > int(n_unita.text()):
			QMessageBox.warning(None, u'WARNING!', u"The value of the '11 NUMERO US CON FUZIONI STRATEGICHE' field is greater than the value of the '10 NUMERO TOTALI UNITA' STRUTTURALI' field!")
			n_edif.setText('')
			n_unita.setText('')
	if (n_unita.text() != '') and (n_edif_gl.text() != ''):
		if int(n_edif_gl.text()) > int(n_unita.text()):
			QMessageBox.warning(None, u'WARNING!', u"The value of the '12 NUMERO US CARATTERIZZATE DA GRANDI LUCI' field is greater than the value of the '10 NUMERO TOTALI UNITA' STRUTTURALI' field!")
			n_edif_gl.setText('')
			n_unita.setText('')

def alert_us_2(dialog):
	n_unita = dialog.findChild(QLineEdit,"n_unita")
	n_murat = dialog.findChild(QLineEdit,"n_murat")
	n_ca = dialog.findChild(QLineEdit,"n_ca")
	n_altre = dialog.findChild(QLineEdit,"n_altre")
	if (n_unita.text() != '') and (n_murat.text() != '') and (n_ca.text() != '') and (n_altre.text() != ''):
		if not int(n_unita.text()) == int(n_murat.text()) + int(n_ca.text()) + int(n_altre.text()):
			QMessageBox.warning(None, u'WARNING!', u"The value of '10 NUMERO TOTALI UNITA' STRUTTURALI' must be equal to the sum of '13 MURATURA', '14 C.A.' and '15 ALTRE STRUTTURE' field!")
			n_murat.setText('')
			n_ca.setText('')
			n_altre.setText('')

def alert_us_3(dialog):
	piani_min = dialog.findChild(QLineEdit,"piani_min")
	piani_max = dialog.findChild(QLineEdit,"piani_max")
	if (piani_min.text() == '') and (piani_max.text() == ''):
		pass
	elif (piani_min.text() != '') and (piani_max.text() != ''):
		if int(piani_min.text()) > int(piani_max.text()):
			QMessageBox.warning(None, u'WARNING!', u"The value of the '18 NUMERI PIANI MINIMO' field is greater than the value of the '19 NUMERO PIANI MASSIMO' field!")
			piani_min.setText('')
			piani_max.setText('')

def disableButton(dialog):
	ID_aggr = dialog.findChild(QLineEdit,"ID_aggr")
	button_box = dialog.findChild(QDialogButtonBox, "button_box")

	if len(ID_aggr.text()) > 1:
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