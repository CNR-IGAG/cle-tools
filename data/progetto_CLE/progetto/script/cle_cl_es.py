# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:		cle_cl_es.py
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


def cl_es(dialog, layer, feature):
	data_es = dialog.findChild(QDateEdit,"data_es")
	today = QDate.currentDate()
	data_es.setDate(today)
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
	anno_prog = dialog.findChild(QLineEdit,"anno_prog")
	anno_cost = dialog.findChild(QLineEdit,"anno_cost")
	esp_pers = dialog.findChild(QLineEdit,"esp_pers")
	interv = dialog.findChild(QComboBox,"interv")
	interv_ann = dialog.findChild(QLineEdit,"interv_ann")
	interv_name = dialog.findChild(QLabel,"interv_name")
	interv_1 = dialog.findChild(QCheckBox,"interv_1")
	interv_2 = dialog.findChild(QCheckBox,"interv_2")
	interv_3 = dialog.findChild(QCheckBox,"interv_3")
	interv_4 = dialog.findChild(QCheckBox,"interv_4")
	interv_5 = dialog.findChild(QCheckBox,"interv_5")
	interv_6 = dialog.findChild(QCheckBox,"interv_6")
	interv_7 = dialog.findChild(QCheckBox,"interv_7")
	isolato = dialog.findChild(QComboBox,"isolato")
	posizio = dialog.findChild(QComboBox,"posizio")
	spec = dialog.findChild(QComboBox,"spec")
	specialis = dialog.findChild(QComboBox,"specialis")
	strutt_ver = dialog.findChild(QComboBox,"strutt_ver")
	tipo_mur = dialog.findChild(QComboBox,"tipo_mur")
	evento_1 = dialog.findChild(QComboBox,"evento_1")
	data_ev_1 = dialog.findChild(QDateEdit,"data_ev_1")
	tipo_1 = dialog.findChild(QComboBox,"tipo_1")
	date_label_1 = dialog.findChild(QLabel,"date_label_1")
	evento_2 = dialog.findChild(QComboBox,"evento_2")
	data_ev_2 = dialog.findChild(QDateEdit,"data_ev_2")
	tipo_2 = dialog.findChild(QComboBox,"tipo_2")
	date_label_2 = dialog.findChild(QLabel,"date_label_2")
	evento_3 = dialog.findChild(QComboBox,"evento_3")
	data_ev_3 = dialog.findChild(QDateEdit,"data_ev_3")
	tipo_3 = dialog.findChild(QComboBox,"tipo_3")
	date_label_3 = dialog.findChild(QLabel,"date_label_3")
	zona_ms = dialog.findChild(QComboBox,"zona_ms")
	inst_name = dialog.findChild(QLabel,"inst_name")
	inst_fran = dialog.findChild(QCheckBox,"inst_fran")
	inst_liq = dialog.findChild(QCheckBox,"inst_liq")
	inst_fag = dialog.findChild(QCheckBox,"inst_fag")
	inst_ced = dialog.findChild(QCheckBox,"inst_ced")
	inst_cav = dialog.findChild(QCheckBox,"inst_cav")
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
	interv_ann.setEnabled(False)
	interv_name.hide()
	interv_1.hide()
	interv_2.hide()
	interv_3.hide()
	interv_4.hide()
	interv_5.hide()
	interv_6.hide()
	interv_7.hide()
	data_ev_1.hide()
	tipo_1.setEnabled(False)
	date_label_1.hide()
	data_ev_2.hide()
	tipo_2.setEnabled(False)
	date_label_2.hide()
	data_ev_3.hide()
	tipo_3.setEnabled(False)
	date_label_3.hide()

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
	anno_prog.textEdited.connect(lambda: update_valore(anno_prog))
	anno_cost.textEdited.connect(lambda: update_valore(anno_cost))
	esp_pers.textEdited.connect(lambda: update_valore(esp_pers))
	interv_ann.textEdited.connect(lambda: update_valore(interv_ann))
	ID_unit.textChanged.connect(lambda: disableButton(dialog))
	ID_aggr.textChanged.connect(lambda: disableButton(dialog))
	anno_prog.editingFinished.connect(lambda: alert_data(dialog))
	anno_cost.editingFinished.connect(lambda: alert_data(dialog))
	isolato.currentIndexChanged.connect(lambda: disablePosizio(dialog))
	spec.currentIndexChanged.connect(lambda: disableSpecialis(dialog))
	strutt_ver.currentIndexChanged.connect(lambda: disableTipo_mur(dialog))
	evento_1.currentIndexChanged.connect(lambda: disableEvento1(dialog))
	evento_2.currentIndexChanged.connect(lambda: disableEvento2(dialog))
	evento_3.currentIndexChanged.connect(lambda: disableEvento3(dialog))
	zona_ms.currentIndexChanged.connect(lambda: disableInstab(dialog))
	interv.currentIndexChanged.connect(lambda: disableInterv(dialog))

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

def alert_data(dialog):
	anno_prog = dialog.findChild(QLineEdit,"anno_prog")
	anno_cost = dialog.findChild(QLineEdit,"anno_cost")
	if (anno_prog.text() == '') and (anno_cost.text() == ''):
		pass
	elif (anno_prog.text() != '') and (anno_cost.text() != ''):
		if int(anno_prog.text()) > int(anno_cost.text()):
			QMessageBox.warning(None, u'WARNING!', u"The value of the 'ANNO DI PROGETTAZIONE' field is greater than the value of the 'ANNO DI FINE COSTRUZIONE' field!")
			anno_prog.setText('')
			anno_cost.setText('')

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

def disableEvento1(dialog):
	evento_1 = dialog.findChild(QComboBox,"evento_1")
	data_ev_1 = dialog.findChild(QDateEdit,"data_ev_1")
	date_label_1 = dialog.findChild(QLabel,"date_label_1")
	tipo_1 = dialog.findChild(QComboBox,"tipo_1")
	if evento_1.currentText() == "":
		data_ev_1.setEnabled(False)
		data_ev_1.setText("")
		tipo_1.setEnabled(False)
	else:
		data_ev_1.show()
		date_label_1.show()
		data_ev_1.setEnabled(True)
		tipo_1.setEnabled(True)

def disableEvento2(dialog):
	evento_2 = dialog.findChild(QComboBox,"evento_2")
	data_ev_2 = dialog.findChild(QDateEdit,"data_ev_2")
	date_label_2 = dialog.findChild(QLabel,"date_label_2")
	tipo_2 = dialog.findChild(QComboBox,"tipo_2")
	if evento_2.currentText() == "":
		data_ev_2.setEnabled(False)
		data_ev_2.setText("")
		tipo_2.setEnabled(False)
	else:
		data_ev_2.show()
		date_label_2.show()
		data_ev_2.setEnabled(True)
		tipo_2.setEnabled(True)

def disableEvento3(dialog):
	evento_3 = dialog.findChild(QComboBox,"evento_3")
	data_ev_3 = dialog.findChild(QDateEdit,"data_ev_3")
	date_label_3 = dialog.findChild(QLabel,"date_label_3")
	tipo_3 = dialog.findChild(QComboBox,"tipo_3")
	if evento_3.currentText() == " ":
		data_ev_3.setEnabled(False)
		data_ev_3.setText("")
		tipo_3.setEnabled(False)
	else:
		data_ev_3.show()
		date_label_3.show()
		data_ev_3.setEnabled(True)
		tipo_3.setEnabled(True)

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

def disableInterv(dialog):
	interv = dialog.findChild(QComboBox,"interv")
	interv_ann = dialog.findChild(QLineEdit,"interv_ann")
	interv_name = dialog.findChild(QLabel,"interv_name")
	interv_1 = dialog.findChild(QCheckBox,"interv_1")
	interv_2 = dialog.findChild(QCheckBox,"interv_2")
	interv_3 = dialog.findChild(QCheckBox,"interv_3")
	interv_4 = dialog.findChild(QCheckBox,"interv_4")
	interv_5 = dialog.findChild(QCheckBox,"interv_5")
	interv_6 = dialog.findChild(QCheckBox,"interv_6")
	interv_7 = dialog.findChild(QCheckBox,"interv_7")
	if interv.currentText() == "SI":
		interv_name.show()
		interv_1.show()
		interv_2.show()
		interv_3.show()
		interv_4.show()
		interv_5.show()
		interv_6.show()
		interv_7.show()
		interv_ann.setEnabled(True)
		interv_1.setEnabled(True)
		interv_2.setEnabled(True)
		interv_3.setEnabled(True)
		interv_4.setEnabled(True)
		interv_5.setEnabled(True)
		interv_6.setEnabled(True)
		interv_7.setEnabled(True)
	else:
		interv_ann.setText("")
		interv_ann.setEnabled(False)
		interv_1.setChecked(False)
		interv_1.setEnabled(False)
		interv_2.setChecked(False)
		interv_2.setEnabled(False)
		interv_3.setChecked(False)
		interv_3.setEnabled(False)
		interv_4.setChecked(False)
		interv_4.setEnabled(False)
		interv_5.setChecked(False)
		interv_5.setEnabled(False)
		interv_6.setChecked(False)
		interv_6.setEnabled(False)
		interv_7.setChecked(False)
		interv_7.setEnabled(False)

def define_lista(cod_list,nome_tab):
	codici = QgsMapLayerRegistry.instance().mapLayersByName(nome_tab)[0]

	for elem in codici.getFeatures(QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)):
		lista_cod=[elem.attributes()[0],elem.attributes()[1]]
		cod_list.append(lista_cod)
	return cod_list

def update_box(Qbox,cod_list):
	Qbox.clear()
	Qbox.addItem("")
	Qbox.model().item(0).setEnabled(False)
	for row in cod_list:
		Qbox.addItem(row[2])

def update_localita(dialog, cod_local, localita):
	localita = dialog.findChild(QComboBox,"localita")
	cod_local = dialog.findChild(QLineEdit,"cod_local")
	TipoIndagine = str(localita.currentText().strip()).split("  -  ")[1]
	cod_local.setText(TipoIndagine)