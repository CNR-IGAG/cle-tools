# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:		tb_esporta_shp.py
# Author:	  Tarquini E.
# Created:	 08-02-2018
#-------------------------------------------------------------------------------

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import *
from qgis.core import *
from qgis.gui import *
import os, sys, webbrowser, shutil, zipfile, sqlite3, constants

FORM_CLASS, _ = uic.loadUiType(os.path.join(
	os.path.dirname(__file__), 'tb_esporta_shp.ui'))


class esporta_shp(QtGui.QDialog, FORM_CLASS):

	def __init__(self, parent=None):
		"""Constructor."""
		self.iface = iface
		super(esporta_shp, self).__init__(parent)
		self.setupUi(self)
		self.plugin_dir = os.path.dirname(__file__)

	def esporta_prog(self):
		self.help_button.clicked.connect(lambda: webbrowser.open('https://www.youtube.com/watch?v=dYcMZSpu6HA&t=2s'))
		LISTA_LIV_2_3 = [["Zone stabili liv 3","Zone stabili liv 2","Stab.shp","Stab","ID_z"],
		["Zone instabili liv 3","Zone instabili liv 2","Instab.shp","Instab","ID_i"],
		["Isobate liv 3", "Isobate liv 2","Isosub.shp", "Isosub", "ID_isosub"]]
		LISTA_QUERY_MZ = ["""INSERT INTO 'sito_puntuale'(pkey_spu, ubicazione_prov, ubicazione_com, ID_SPU, indirizzo, coord_X, coord_Y,
		mod_identcoord, desc_modcoord, quota_slm, modo_quota, data_sito, note_sito) SELECT pkuid, ubicazione_prov, ubicazione_com,
		id_spu, indirizzo, coord_x, coord_y, mod_identcoord, desc_modcoord, quota_slm, modo_quota, data_sito, note_sito FROM A.sito_puntuale;""",
		"""INSERT INTO 'indagini_puntuali'(pkey_indpu, id_spu, classe_ind, tipo_ind, ID_INDPU, id_indpuex, arch_ex, note_ind, prof_top,
		prof_bot, spessore, quota_slm_top, quota_slm_bot, data_ind, doc_pag, doc_ind) SELECT pkuid, id_spu, classe_ind, tipo_ind, id_indpu,
		id_indpuex, arch_ex, note_ind, prof_top, prof_bot, spessore, quota_slm_top, quota_slm_bot, data_ind, doc_pag, doc_ind FROM A.indagini_puntuali;""",
		"""INSERT INTO 'parametri_puntuali'(pkey_parpu, id_indpu, tipo_parpu, ID_PARPU, prof_top, prof_bot, spessore, quota_slm_top, quota_slm_bot, valore,
		attend_mis, tab_curve, note_par, data_par) SELECT pkuid, id_indpu, tipo_parpu, id_parpu, prof_top, prof_bot, spessore, quota_slm_top, quota_slm_bot,
		valore, attend_mis, tab_curve, note_par, data_par FROM A.parametri_puntuali;""",
		"""INSERT INTO 'curve'(pkey_curve, id_parpu, cond_curve, varx, vary) SELECT pkuid, id_parpu, cond_curve, varx, vary FROM A.curve;""",
		"""INSERT INTO 'sito_lineare'(pkey_sln, ubicazione_prov, ubicazione_com, ID_SLN, Acoord_X, Acoord_Y, Bcoord_X, Bcoord_Y, mod_identcoord, desc_modcoord,
		Aquota, Bquota, data_sito, note_sito) SELECT pkuid, ubicazione_prov, ubicazione_com, id_sln, acoord_x, acoord_y, bcoord_x, bcoord_y, mod_identcoord,
		desc_modcoord, aquota, bquota, data_sito, note_sito FROM A.sito_lineare;""",
		"""INSERT INTO 'indagini_lineari'(pkey_indln, id_sln, classe_ind, tipo_ind, ID_INDLN, id_indlnex, arch_ex, note_indln, data_ind, doc_pag, doc_ind)
		SELECT pkuid, id_sln, classe_ind, tipo_ind, id_indln, id_indlnex, arch_ex, note_indln, data_ind, doc_pag, doc_ind FROM A.indagini_lineari;""",
		"""INSERT INTO 'parametri_lineari'(pkey_parln, id_indln, tipo_parln, ID_PARLN, prof_top, prof_bot, spessore, quota_slm_top, quota_slm_bot, valore,
		attend_mis, note_par, data_par) SELECT pkuid, id_indln, tipo_parln, id_parln, prof_top, prof_bot, spessore, quota_slm_top, quota_slm_bot, valore,
		attend_mis, note_par, data_par FROM A.parametri_lineari;"""]
		LISTA_QUERY_CLE = ["""INSERT INTO 'indice'(data_in,regione,cod_reg,provincia,cod_prov,comune,cod_com,soggetto,ufficio,responsabile,ID_CLE) SELECT data_in,
		regione,cod_reg,provincia,cod_prov,comune,cod_com,soggetto,ufficio,responsabile,ID_CLE FROM A.indice;""",
		"""INSERT INTO 'cl_es'(data_es,regione,cod_reg,provincia,cod_prov,comune,cod_com,localita,cod_local,sezione,ID_aggr ,ID_unit ,ID_area,ID_infra_a,ID_infra_b,
		ID_infra_c,ID_infra_d,indirizzo,civico,denom,isolato,posizio,fronte,spec,specialis,n_piani,n_interr,alt_piano,alt_totale,vol_unico,superf_m,strutt_ver,tipo_mur,
		cord_cat,pilastri,pilotis,sopraelev,danno,stato_man,pr_pubb,pr_priv,morf,ubic_sotto,ubic_sopra,zona_ms,inst_fran,inst_liq,inst_fag,inst_ced,inst_cav,frana_ar,
		frana_mon,frana_val,pai,alluvio,ID_edif,emerg_1,emerg_2,emerg_3,emerg_4,emerg_5,emerg_6,uso_orig,uso_att,anno_prog,anno_cost,esp_pers,esp_ore,esp_mes,interv,
		interv_ann,interv_1,interv_2,interv_3,interv_4,interv_5,interv_6,interv_7,evento_1,data_ev_1,tipo_1,evento_2,data_ev_2,tipo_2,evento_3,data_ev_3,tipo_3,verif_sism,ID_ES)
		SELECT data_es,regione,cod_reg,provincia,cod_prov,comune,cod_com,localita,cod_local,sezione,ID_aggr ,ID_unit ,ID_area,ID_infra_a,ID_infra_b,ID_infra_c,ID_infra_d,
		indirizzo,civico,denom,isolato,posizio,fronte,spec,specialis,n_piani,n_interr,alt_piano,alt_totale,vol_unico,superf_m,strutt_ver,tipo_mur,cord_cat,pilastri,pilotis,
		sopraelev,danno,stato_man,pr_pubb,pr_priv,morf,ubic_sotto,ubic_sopra,zona_ms,inst_fran,inst_liq,inst_fag,inst_ced,inst_cav,frana_ar,frana_mon,frana_val,pai,alluvio,
		ID_edif,emerg_1,emerg_2,emerg_3,emerg_4,emerg_5,emerg_6,uso_orig,uso_att,anno_prog,anno_cost,esp_pers,esp_ore,esp_mes,interv,interv_ann,interv_1,interv_2,interv_3,
		interv_4,interv_5,interv_6,interv_7,evento_1,data_ev_1,tipo_1,evento_2,data_ev_2,tipo_2,evento_3,data_ev_3,tipo_3,verif_sism,ID_ES FROM A.cl_es;""",
		"""INSERT INTO 'cl_ae'(data_ae,regione,cod_reg,provincia,cod_prov,comune,cod_com,localita,cod_local,ID_area,ID_infra_a,ID_infra_b,ID_infra_c,ID_infra_d,denom,tipo_area,piano,
		anno_piano, n_aggreg,n_manuf,superf,rett_max,rett_min,pav_per,infra_acq,infra_ele,infra_fog,morf,ubic_sotto,ubic_sopra,zona_ms,inst_fran,inst_liq,inst_fag,inst_ced,inst_cav,
		frana_AE,frana_mon,frana_val,falda,acq_sup,pai,alluvio,ID_AE) SELECT data_ae,regione,cod_reg,provincia,cod_prov,comune,cod_com,localita,cod_local,ID_area,ID_infra_a,ID_infra_b,
		ID_infra_c,ID_infra_d,denom,tipo_area,piano,anno_piano, n_aggreg,n_manuf,superf,rett_max,rett_min,pav_per,infra_acq,infra_ele,infra_fog,morf,ubic_sotto,ubic_sopra,zona_ms,
		inst_fran,inst_liq,inst_fag,inst_ced,inst_cav,frana_AE,frana_mon,frana_val,falda,acq_sup,pai,alluvio,ID_AE FROM A.cl_ae;""",
		"""INSERT INTO 'cl_ac'(data_ac,regione,cod_reg,provincia,cod_prov,comune,cod_com,localita,cod_local,tipo_infra,ID_infra,strade_a,strade_b,strade_c,strade_d,strade_e,strade_f,
		largh_max,largh_min,lungh,lungh_vuo,pav_per,ost_disc,n_aggreg,n_manuf,el_ferrov,el_pont,el_tunn,el_pont_at,el_muri,pendenza,morf,ubic_sotto,ubic_sopra,zona_ms,inst_fran,inst_liq,
		inst_fag,inst_ced,inst_cav,frana_AC,frana_mon,frana_val,falda,acq_sup,pai,alluvio,ID_AC) SELECT data_ac,regione,cod_reg,provincia,cod_prov,comune,cod_com,localita,cod_local,
		tipo_infra,ID_infra,strade_a,strade_b,strade_c,strade_d,strade_e,strade_f,largh_max,largh_min,lungh,lungh_vuo,pav_per,ost_disc,n_aggreg,n_manuf,el_ferrov,el_pont,el_tunn,
		el_pont_at,el_muri,pendenza,morf,ubic_sotto,ubic_sopra,zona_ms,inst_fran,inst_liq,inst_fag,inst_ced,inst_cav,frana_AC,frana_mon,frana_val,falda,acq_sup,pai,alluvio,ID_AC FROM A.cl_ac;""",
		"""INSERT INTO 'cl_as'(data_as,regione,cod_reg,provincia,cod_prov,comune,cod_com,localita,cod_local,sezione,ID_aggr,ID_area,ID_infra_a,ID_infra_b,ID_infra_c,ID_infra_d,n_unita,
		n_edif,n_edif_gl,n_murat,n_ca,n_altre,altezza,superf,piani_min,piani_max,lungh_fron,us_interf,conn_volte,conn_rifus,regol_1,regol_2,regol_3,regol_4,regol_5,vuln_1,vuln_2,vuln_3,
		vuln_4,vuln_5,vuln_6,rinfor_1,rinfor_2,morf,ubic_sotto,ubic_sopra,zona_ms,inst_fran,inst_liq,inst_fag,inst_ced,inst_cav,frana_AS,frana_mon,frana_val,pai,alluvio,ID_AS) SELECT data_as,
		regione,cod_reg,provincia,cod_prov,comune,cod_com,localita,cod_local,sezione,ID_aggr,ID_area,ID_infra_a,ID_infra_b,ID_infra_c,ID_infra_d,n_unita,n_edif,n_edif_gl,n_murat,n_ca,n_altre,
		altezza,superf,piani_min,piani_max,lungh_fron,us_interf,conn_volte,conn_rifus,regol_1,regol_2,regol_3,regol_4,regol_5,vuln_1,vuln_2,vuln_3,vuln_4,vuln_5,vuln_6,rinfor_1,rinfor_2,morf,
		ubic_sotto,ubic_sopra,zona_ms,inst_fran,inst_liq,inst_fag,inst_ced,inst_cav,frana_AS,frana_mon,frana_val,pai,alluvio,ID_AS FROM A.cl_as;""",
		"""INSERT INTO 'cl_us'(data_us,regione,cod_reg,provincia,cod_prov,comune,cod_com,localita,cod_local,sezione,ID_aggr,ID_unit,ID_area,ID_infra_a,ID_infra_b,ID_infra_c,ID_infra_d,
		indirizzo,civico,isolato,posizio,fronte,spec,specialis,n_piani,n_interr,alt_piano,alt_totale,vol_unico,superf_m,strutt_ver,tipo_mur,cord_cat,pilastri,pilotis,sopraelev,danno,stato_man,
		pr_pubb,pr_priv,morf,ubic_sotto,ubic_sopra,zona_ms,inst_fran,inst_liq,inst_fag,inst_ced,inst_cav,frana_ar,frana_mon,frana_val,pai,alluvio,uso_att,uso_a,uso_a_1,uso_b,uso_b_1,uso_c,uso_c_1,
		uso_d,uso_d_1,uso_e,uso_e_1,uso_f,uso_f_1,uso_g,uso_g_1,epoca_1,epoca_2,epoca_3,epoca_4,epoca_5,epoca_6,epoca_7,epoca_8,utilizz,occupanti,ID_US) SELECT data_us,regione,cod_reg,provincia,
		cod_prov,comune,cod_com,localita,cod_local,sezione,ID_aggr,ID_unit,ID_area,ID_infra_a,ID_infra_b,ID_infra_c,ID_infra_d,indirizzo,civico,isolato,posizio,fronte,spec,specialis,n_piani,n_interr,
		alt_piano,alt_totale,vol_unico,superf_m,strutt_ver,tipo_mur,cord_cat,pilastri,pilotis,sopraelev,danno,stato_man,pr_pubb,pr_priv,morf,ubic_sotto,ubic_sopra,zona_ms,inst_fran,inst_liq,inst_fag,
		inst_ced,inst_cav,frana_ar,frana_mon,frana_val,pai,alluvio,uso_att,uso_a,uso_a_1,uso_b,uso_b_1,uso_c,uso_c_1,uso_d,uso_d_1,uso_e,uso_e_1,uso_f,uso_f_1,uso_g,uso_g_1,epoca_1,epoca_2,epoca_3,
		epoca_4,epoca_5,epoca_6,epoca_7,epoca_8,utilizz,occupanti,ID_US FROM A.cl_us;"""]

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
					input_name = out_dir + os.sep + "progetto_shapefile"
					output_name = out_dir + os.sep + in_dir.split("/")[-1]
					zip_ref = zipfile.ZipFile(self.plugin_dir + os.sep + "data" + os.sep + "progetto_shapefile.zip", 'r')
					zip_ref.extractall(out_dir)
					zip_ref.close()
					os.rename(input_name, output_name)

					root = QgsProject.instance().layerTreeRoot()

					for chiave, valore in constants.POSIZIONE.iteritems():
						sourceLYR = QgsMapLayerRegistry.instance().mapLayersByName(chiave)[0]
						QgsVectorFileWriter.writeAsVectorFormat(sourceLYR ,output_name + os.sep + valore[0] + os.sep + valore[1],"utf-8",None,"ESRI Shapefile")
						selected_layer = QgsVectorLayer(output_name + os.sep + valore[0] + os.sep + valore[1] + ".shp", valore[1], 'ogr')
						if chiave == "Zone stabili liv 2" or chiave == "Zone instabili liv 2" or chiave == "Zone stabili liv 3" or chiave == "Zone instabili liv 3":
							pass
						elif chiave == "Siti lineari" or chiave == "Siti puntuali":
							self.esporta([0, ['id_spu','id_sln']], selected_layer)
						elif chiave == "Limiti comunali" or chiave == "Infrastrutture di accessibilita' e connessione" or chiave == "Aree di emergenza" or chiave == "Aggregati strutturali" or chiave == "Edifici strategici" or chiave == "Unita' strutturali":
							self.esporta([0, ["cod_prov", "cod_com", "ID_aggr", "ID_unit", "ID_ES", "ID_area", "ID_AE", "ID_infra", "ID_AC", "ID_AS", "ID_US"]], selected_layer)
						else:
							self.esporta([1, ['pkuid']], selected_layer)

					for l23_value in LISTA_LIV_2_3:
						sourceLYR_1 = QgsMapLayerRegistry.instance().mapLayersByName(l23_value[0])[0]
						QgsVectorFileWriter.writeAsVectorFormat(sourceLYR_1 ,output_name + os.sep + "MS23" + os.sep + l23_value[2],"utf-8",None,"ESRI Shapefile")
						sourceLYR_2 = QgsMapLayerRegistry.instance().mapLayersByName(l23_value[1])[0]
						MS23_stab = QgsVectorLayer(output_name + os.sep + "MS23" + os.sep + l23_value[2], l23_value[3], 'ogr')
						features = []
						for feature in sourceLYR_2.getFeatures():
							features.append(feature)
						MS23_stab.startEditing()
						data_provider = MS23_stab.dataProvider()
						data_provider.addFeatures(features)
						MS23_stab.commitChanges()
						selected_layer_1 = QgsVectorLayer(output_name + os.sep + "MS23" + os.sep + l23_value[2], l23_value[3], 'ogr')
						self.esporta([1, ['pkuid']], selected_layer_1)

					if os.path.exists(in_dir + os.sep + "allegati" + os.sep + "Plot"):
						shutil.copytree(in_dir + os.sep + "allegati" + os.sep + "Plot", output_name + os.sep + "Plot")
					if os.path.exists(in_dir + os.sep + "allegati" + os.sep + "Documenti"):
						shutil.copytree(in_dir + os.sep + "allegati" + os.sep + "Documenti", output_name + os.sep + "Indagini" + os.sep + "Documenti")
					if os.path.exists(in_dir + os.sep + "allegati" + os.sep + "Spettri"):
						shutil.copytree(in_dir + os.sep + "allegati" + os.sep + "Spettri", output_name + os.sep + "MS23" + os.sep + "Spettri")
					if os.path.exists(in_dir + os.sep + "allegati" + os.sep + "altro"):
						shutil.copytree(in_dir + os.sep + "allegati" + os.sep + "altro", output_name + os.sep + "altro")

					for file_name in os.listdir(in_dir + os.sep + "allegati"):
						if file_name.endswith(".txt"):
							shutil.copyfile(in_dir + os.sep + "allegati" + os.sep + file_name, output_name + os.sep + file_name)

					dir_gdb_mz = output_name + os.sep + "Indagini" + os.sep + "CdI_Tabelle.sqlite"
					orig_gdb =  in_dir + os.sep + "db" + os.sep + "indagini.sqlite"
					conn = sqlite3.connect(dir_gdb_mz)
					sql = """ATTACH '""" + orig_gdb + """' AS A;"""
					conn.execute(sql)
					for query in LISTA_QUERY_MZ:
						conn.execute(query)
						conn.commit()
					conn.close()

					dir_gdb_cle = output_name + os.sep + "CLE" + os.sep + "CLE_db.sqlite"
					orig_gdb =  in_dir + os.sep + "db" + os.sep + "indagini.sqlite"
					conn = sqlite3.connect(dir_gdb_cle)
					sql = """ATTACH '""" + orig_gdb + """' AS A;"""
					conn.execute(sql)
					for query in LISTA_QUERY_CLE:
						conn.execute(query)
						conn.commit()
					conn.close()

					QMessageBox.information(None, u'INFORMATION!', u"The project has been exported!")

				else:
					QMessageBox.warning(None, u'WARNING!', u"The selected directory does not exist!")

			except Exception as z:
				QMessageBox.critical(None, u'ERROR!', u'Error:\n"' + str(z) + '"')

	def disableButton(self):
		conteggio = 0
		check_campi = [self.dir_output.text()]
		check_value = []

		layers = self.iface.legendInterface().layers()
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

		if conteggio > 23 and campi > 0:
			self.button_box.setEnabled(True)
			self.alert_text.hide()
		elif conteggio > 23 and campi == 0:
			self.button_box.setEnabled(False)
			self.alert_text.hide()
		else:
			self.button_box.setEnabled(False)
			self.alert_text.show()

	def esporta(self, list_attr, selected_layer):

		field_ids = []
		fieldnames = set(list_attr[1])
		if list_attr[0] == 0:
			for field in selected_layer.fields():
				if field.name() not in fieldnames:
					field_ids.append(selected_layer.fieldNameIndex(field.name()))
			selected_layer.dataProvider().deleteAttributes(field_ids)
			selected_layer.updateFields()
		elif list_attr[0] == 1:
			for field in selected_layer.fields():
				if field.name() in fieldnames:
					field_ids.append(selected_layer.fieldNameIndex(field.name()))
			selected_layer.dataProvider().deleteAttributes(field_ids)
			selected_layer.updateFields()
