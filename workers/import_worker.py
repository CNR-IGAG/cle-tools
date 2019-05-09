# -*- coding: utf-8 -*-

from MzSTools.constants import *
import os, shutil, sqlite3, csv
from qgis.core import QgsVectorLayer, QgsFeatureRequest, QgsField, QgsVectorJoinInfo, QgsExpressionContext, QgsExpressionContextScope, QgsMessageLog
from qgis.utils import QgsExpression

from abstract_worker import AbstractWorker, UserAbortedNotification


class ImportWorker(AbstractWorker):
	'''Worker class handling data import from existing project'''

	def __init__(self, proj_abs_path, in_dir, tab_dir, map_registry_instance):
		AbstractWorker.__init__(self)
#		 self.steps = steps
		self.proj_abs_path = proj_abs_path
		self.in_dir = in_dir
		self.tab_dir = tab_dir
		self.map_registry_instance = map_registry_instance

		self.current_step = 1
		self.check_sito_p = True
		self.check_sito_l = True

	def work(self):
		path_tabelle = self.proj_abs_path + os.sep + "allegati" + os.sep + "altro"
		z_list = []

		# calculate steps
		total_steps = len(POSIZIONE) + 5

		# step 1 (preparing data)
		###############################################
		self.set_message.emit('Creating folders...')

		if os.path.exists(path_tabelle + os.sep + "Indagini"):
			shutil.rmtree(path_tabelle + os.sep + "Indagini")

		os.makedirs(path_tabelle + os.sep + "Indagini")
		self.copy_files(self.in_dir + os.sep + "Indagini", path_tabelle + os.sep + "Indagini")

		for nome_tab in LISTA_TAB:
			if os.path.exists(path_tabelle + os.sep + nome_tab):
				os.remove(path_tabelle + os.sep + nome_tab)

		self.set_log_message.emit('Folder structure -> OK\n')

		self.set_message.emit('Copying tables...')
		self.copy_files(self.tab_dir, path_tabelle)

		# end step 1
		if self.killed:
			raise UserAbortedNotification('USER Killed')
		self.current_step = self.current_step + 1
		self.progress.emit(self.current_step * 100/total_steps)

		#self.set_log_message.emit('Tables copy -> OK\n')

		# step 2 (inserting features)
		###############################################
		for chiave, valore in POSIZIONE.iteritems():

			if not os.path.exists(self.in_dir + os.sep + valore[0] + os.sep + valore[1] + ".shp"):
				self.set_log_message.emit("'" + chiave + "' shapefile does not exist!\n")
				continue

			sourceLYR = QgsVectorLayer(self.in_dir + os.sep + valore[0] + os.sep + valore[1] + ".shp", valore[1], 'ogr')
			destLYR = self.map_registry_instance.mapLayersByName(chiave)[0]

			commonFields = self.attribute_adaptor(destLYR,sourceLYR)

##			if chiave == "Siti puntuali":
##				if os.path.exists(path_tabelle + os.sep + 'Sito_Puntuale.txt'):
##					self.insert_siti(sourceLYR, path_tabelle + os.sep + 'Sito_Puntuale.txt', "Sito puntuale")
##					self.set_message.emit("'" + chiave + "' shapefile has been copied!")
##					self.set_log_message.emit("'" + chiave + "' shapefile has been copied!\n")
##					z_list.append("Sito_Puntuale")
##				else:
##					self.set_log_message.emit("Table 'Sito_Puntuale.txt' does not exist!\n")
##					self.check_sito_p = False
##
##			elif chiave == "Siti lineari":
##				if os.path.exists(path_tabelle + os.sep + 'Sito_Lineare.txt'):
##					self.insert_siti(sourceLYR, path_tabelle + os.sep + 'Sito_Lineare.txt', "Sito lineare")
##					self.set_message.emit("'" + chiave + "' shapefile has been copied!")
##					self.set_log_message.emit("'" + chiave + "' shapefile has been copied!\n")
##					z_list.append("Sito_Lineare")
##				else:
##					self.set_log_message.emit("Table 'Sito_Lineare.txt' does not exist!\n")
##					self.check_sito_l = False
##
##			elif chiave == "Zone stabili liv 2" or chiave == "Zone instabili liv 2":
##				sourceFeatures = sourceLYR.getFeatures(QgsFeatureRequest(QgsExpression( " \"LIVELLO\" = 2 " )))
##				self.calc_layer(sourceFeatures, destLYR, commonFields)
##				self.set_message.emit("'" + chiave + "' shapefile has been copied!")
##				self.set_log_message.emit("'" + chiave + "' shapefile has been copied!\n")
##
##			elif chiave == "Zone stabili liv 3" or chiave == "Zone instabili liv 3":
##				sourceFeatures = sourceLYR.getFeatures(QgsFeatureRequest(QgsExpression( " \"LIVELLO\" = 3 " )))
##				self.calc_layer(sourceFeatures, destLYR, commonFields)
##				self.set_message.emit("'" + chiave + "' shapefile has been copied!")
##				self.set_log_message.emit("'" + chiave + "' shapefile has been copied!\n")

			if chiave == "Infrastrutture di accessibilita' e connessione":
				if os.path.exists(path_tabelle + os.sep + 'scheda_AC.txt'):
					self.insert_siti(sourceLYR, path_tabelle + os.sep + 'scheda_AC.txt', "CLE AC")
					self.set_message.emit("'" + chiave + "' shapefile has been copied!")
					self.set_log_message.emit("'" + chiave + "' shapefile has been copied!\n")
				else:
					self.set_log_message.emit("Table 'scheda_AC.txt' does not exist!\n")

			elif chiave == "Aree di emergenza":
				if os.path.exists(path_tabelle + os.sep + 'scheda_AE.txt'):
					self.insert_siti(sourceLYR, path_tabelle + os.sep + 'scheda_AE.txt', "CLE AE")
					self.set_message.emit("'" + chiave + "' shapefile has been copied!")
					self.set_log_message.emit("'" + chiave + "' shapefile has been copied!\n")
				else:
					self.set_log_message.emit("Table 'scheda_AE.txt' does not exist!\n")

			elif chiave == "Aggregati strutturali":
				if os.path.exists(path_tabelle + os.sep + 'scheda_AS.txt'):
					self.insert_siti(sourceLYR, path_tabelle + os.sep + 'scheda_AS.txt', "CLE AS")
					self.set_message.emit("'" + chiave + "' shapefile has been copied!")
					self.set_log_message.emit("'" + chiave + "' shapefile has been copied!\n")
				else:
					self.set_log_message.emit("Table 'scheda_AS.txt' does not exist!\n")

			elif chiave == "Edifici strategici":
				if os.path.exists(path_tabelle + os.sep + 'scheda_ES.txt'):
					self.insert_siti(sourceLYR, path_tabelle + os.sep + 'scheda_ES.txt', "CLE ES")
					self.set_message.emit("'" + chiave + "' shapefile has been copied!")
					self.set_log_message.emit("'" + chiave + "' shapefile has been copied!\n")
				else:
					self.set_log_message.emit("Table 'scheda_ES.txt' does not exist!\n")

			elif chiave == "Unita' strutturali":
				if os.path.exists(path_tabelle + os.sep + 'scheda_US.txt'):
					self.insert_siti(sourceLYR, path_tabelle + os.sep + 'scheda_US.txt', "CLE US")
					self.set_message.emit("'" + chiave + "' shapefile has been copied!")
					self.set_log_message.emit("'" + chiave + "' shapefile has been copied!\n")
				else:
					self.set_log_message.emit("Table 'scheda_US.txt' does not exist!\n")

			elif chiave == "Comune del progetto":
				pass
			else:
				sourceFeatures = sourceLYR.getFeatures()
				self.calc_layer(sourceFeatures, destLYR, commonFields)
				self.set_log_message.emit("'" + chiave + "' shapefile has been copied!\n")

			if self.killed:
				break

			self.current_step = self.current_step + 1
			self.progress.emit(self.current_step * 100/total_steps)
		# end for

		if self.killed:
			raise UserAbortedNotification('USER Killed')

		#self.set_log_message.emit('Insert features -> OK\n')
		# end inserting features

		# step 3 (inserting indagini_puntuali and related data)
		#######################################################
		if self.check_sito_p is True and os.path.exists(path_tabelle + os.sep + "Indagini_Puntuali.txt"):
			z_list.append("Indagini_Puntuali")
			self.insert_table("indagini_puntuali", path_tabelle + os.sep + "Indagini_Puntuali.txt")
			self.set_log_message.emit("'Indagini_Puntuali' table has been copied!\n")

			if os.path.exists(path_tabelle + os.sep + "Parametri_Puntuali.txt"):
				z_list.append("Parametri_Puntuali")
				self.insert_table("parametri_puntuali", path_tabelle + os.sep + "Parametri_Puntuali.txt")
				self.set_log_message.emit("'Parametri_Puntuali' table has been copied!\n")

				if os.path.exists(path_tabelle + os.sep + "Curve.txt"):
					z_list.append("Curve")
					self.insert_table("curve", path_tabelle + os.sep + "Curve.txt")
					self.set_log_message.emit("'Curve' table has been copied!\n")

		# end inserting indagini puntuali
		if self.killed:
			raise UserAbortedNotification('USER Killed')
		self.current_step = self.current_step + 1
		self.progress.emit(self.current_step * 100/total_steps)

		# step 4 (inserting indagini lineari and related data)
		######################################################
		if self.check_sito_l is True and os.path.exists(path_tabelle + os.sep + "Indagini_Lineari.txt"):
			z_list.append("Indagini_Lineari")
			self.insert_table("indagini_lineari", path_tabelle + os.sep + "Indagini_Lineari.txt")
			self.set_log_message.emit("'Indagini_Lineari' table has been copied!\n")

			if os.path.exists(path_tabelle + os.sep + "Parametri_Lineari.txt"):
				z_list.append("Parametri_Lineari")
				self.insert_table("parametri_lineari", path_tabelle + os.sep + "Parametri_Lineari.txt")
				self.set_log_message.emit("'Parametri_Lineari' table has been copied!\n")

		if self.check_sito_p is False:
			self.set_log_message.emit("'Ind_pu' layer and/or 'Sito_Puntuale' table are not present! The correlated surveys and parameters tables will not be copied!\n\n")
		if self.check_sito_l is False:
			self.set_log_message.emit("'Ind_ln' layer and/or 'Sito_Lineare' table are not present! The correlated surveys and parameters tables will not be copied!\n\n")
		if self.check_sito_p is True and self.check_sito_l is True:
			tab_mancanti = list(set(LISTA_TAB) - set(z_list))
			for t_lost in tab_mancanti:
				self.set_log_message.emit("'" + t_lost + "' table does not exist!\n")

		# end inserting indagini lineari
		if self.killed:
			raise UserAbortedNotification('USER Killed')
		self.current_step = self.current_step + 1
		self.progress.emit(self.current_step * 100/total_steps)

		# step 5 (miscellaneous files and cleanup)
		###############################################
		self.set_message.emit('Adding miscellaneous files...')

		dizio_folder = {"Plot" : ["OLD_Plot", self.proj_abs_path + os.sep + "allegati" + os.sep + "Plot", self.in_dir + os.sep + "Plot"], "Documenti" : ["OLD_Documenti", self.proj_abs_path + os.sep + "allegati" + os.sep + "Documenti", self.in_dir + os.sep + "Indagini" + os.sep + "Documenti"], "Spettri" : ["OLD_Spettri", self.proj_abs_path + os.sep + "allegati" + os.sep + "Spettri", self.in_dir + os.sep + "MS23" + os.sep + "Spettri"]}

		for chiave_fold, valore_fold in dizio_folder.iteritems():
			self.set_message.emit("Copying '" + chiave_fold + "' folder")
			if os.path.exists(valore_fold[2]):
				if os.path.exists(self.proj_abs_path + os.sep + "allegati" + os.sep + chiave_fold):
					shutil.rmtree(self.proj_abs_path + os.sep + "allegati" + os.sep + chiave_fold)
					shutil.copytree(valore_fold[2], valore_fold[1])
				else:
					shutil.copytree(self.in_dir + os.sep + chiave_fold, self.proj_abs_path + os.sep + "allegati" + os.sep + chiave_fold)
				self.set_log_message.emit("Folder '" + chiave_fold + " has been copied!\n")
			else:
				self.set_log_message.emit("Folder '" + chiave_fold + "' does not exist!")

			if self.killed:
				break

		self.set_message.emit('Final cleanup...')
		shutil.rmtree(self.proj_abs_path + os.sep + "allegati" + os.sep + "altro")
		os.makedirs(self.proj_abs_path + os.sep + "allegati" + os.sep + "altro")

		# end miscellaneous files and cleanup
		if self.killed:
			raise UserAbortedNotification('USER Killed')
		self.current_step = self.current_step + 1
		self.progress.emit(self.current_step * 100/total_steps)

		return 'Import completed!'

	def attribute_adaptor(self, targetLayer, sourceLayer):
		targetLayerFields = []
		sourceLayerFields = []
		primaryKeyList = []

		for index in targetLayer.dataProvider().pkAttributeIndexes():
			primaryKeyList.append(targetLayer.dataProvider().fields().at(index).name())

		for field in sourceLayer.dataProvider().fields().toList():
			sourceLayerFields.append(field.name())

		for field in targetLayer.dataProvider().fields().toList():
			targetLayerFields.append(field.name())

		commonFields = list(set(sourceLayerFields) & set(targetLayerFields))
		commonFields = list(set(commonFields)-set(primaryKeyList))

		return commonFields

	def attribute_fill(self, qgsFeature, targetLayer, commonFields):

		featureFields = {}

		for field in qgsFeature.fields().toList():
			if field.name() == "desc_modco":
				featureFields["desc_modcoord"] = qgsFeature[field.name()]
			elif field.name() == "mod_identc":
				featureFields["mod_identcoord"] = qgsFeature[field.name()]
			elif field.name() == "ub_prov":
				featureFields["ubicazione_prov"] = qgsFeature[field.name()]
			elif field.name() == "ub_com":
				featureFields["ubicazione_com"] = qgsFeature[field.name()]
			elif field.name() == "ID_SPU":
				featureFields["id_spu"] = qgsFeature[field.name()]
			elif field.name() == "ID_SLN":
				featureFields["id_sln"] = qgsFeature[field.name()]
			else:
				featureFields[field.name()] = qgsFeature[field.name()]

		qgsFeature.setFields(targetLayer.dataProvider().fields())
		if commonFields:
			for fieldName in commonFields:
				qgsFeature[fieldName]=featureFields[fieldName]

		return qgsFeature

	def calc_layer(self, sourceFeatures, destLYR, commonFields):

		featureList = []
		for feature in sourceFeatures:
			geom = feature.geometry()
			if geom:
				err = geom.validateGeometry()
				if not err:
					modifiedFeature = self.attribute_fill(feature,destLYR,commonFields)
					featureList.append(modifiedFeature)
				else:
					self.set_log_message.emit("  Geometry error (feature %d will not be copied)\n" % (feature.id()+1))

		data_provider = destLYR.dataProvider()
		current_feature = 1
		for f in featureList:
			self.set_message.emit(destLYR.name() + ": inserting feature " + str(current_feature) + "/" + str(len(featureList)))
			data_provider.addFeatures([f])
			current_feature = current_feature + 1
			if self.killed:
				break

		if self.killed:
			raise UserAbortedNotification('USER Killed')

	def insert_siti(self, vector_layer, txt_table, sito_type):

		if sito_type == "Sito puntuale":
			id_field_name = "ID_SPU"
			tab_name = "sito_puntuale"
		elif sito_type == "Sito lineare":
			id_field_name = "ID_SLN"
			tab_name = "sito_lineare"
		if sito_type == "CLE AC":
			id_field_name = "ID_AC"
			tab_name = "cl_ac"
		elif sito_type == "CLE AE":
			id_field_name = "ID_AE"
			tab_name = "cl_as"
		elif sito_type == "CLE AS":
			id_field_name = "ID_AS"
			tab_name = "cl_es"
		elif sito_type == "CLE ES":
			id_field_name = "ID_ES"
			tab_name = "cl_es"
		elif sito_type == "CLE US":
			id_field_name = "ID_US"
			tab_name = "cl_us"

		path_db = self.proj_abs_path + os.sep + "db" + os.sep + "indagini.sqlite"
		dict_sito = {}
		conn = sqlite3.connect(path_db)
		conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
		conn.enable_load_extension(True)

		try:
			conn.execute('SELECT load_extension("mod_spatialite")')
			cur = conn.cursor()

			# drop insert trigger to speed up import process
			# TODO: causes QGIS crash
			# cur.execute("DROP TRIGGER ins_data_s_point" if tab_name == "sito_puntuale" else "DROP TRIGGER ins_data_s_line")

			with open(txt_table,'r') as table:
				dr = csv.DictReader(table, delimiter=';', quotechar='"')
				current_feature = 1
				row_num = len(list(dr))
				# restart reading file after line count
				table.seek(0)
				next(dr)
				for i in dr:
					self.set_message.emit("%s: inserting feature %s/%s" % (sito_type, str(current_feature), str(row_num)))

					# transform empty strings to None to circumvent db CHECKs
					for k in i:
						if i[k] == "":
							i[k] = None

					# populate dict_sito and get geom from vector layer
					for key in i.keys():
						dict_sito[key] = i[key]
						if key == id_field_name:
							for feature in vector_layer.getFeatures():
								if feature[id_field_name] == dict_sito[id_field_name]:
									geom = feature.geometry().exportToWkt()

					if sito_type == "Sito puntuale":
						cur.execute("INSERT INTO sito_puntuale (id_spu, geom) VALUES (?, GeomFromText(?, 32633))", (dict_sito["ID_SPU"], geom))
						lastid = cur.lastrowid
						cur.execute('''UPDATE sito_puntuale SET pkuid = ?, indirizzo = ?, mod_identcoord = ?,
							desc_modcoord = ?, quota_slm = ?, modo_quota = ?, data_sito = ?, note_sito = ?
							WHERE pkuid = ?;''',  (dict_sito["pkey_spu"], dict_sito["indirizzo"], dict_sito["mod_identcoord"],
							dict_sito["desc_modcoord"], dict_sito["quota_slm"], dict_sito["modo_quota"],
							dict_sito["data_sito"], dict_sito["note_sito"], lastid))
					elif sito_type == "Sito lineare":
						cur.execute("INSERT INTO sito_lineare (id_sln, geom) VALUES (?, GeomFromText(?, 32633))", (dict_sito["ID_SLN"], geom))
						lastid = cur.lastrowid
						cur.execute('''UPDATE sito_lineare SET pkuid = ?, mod_identcoord = ?,
							desc_modcoord = ?, aquota = ?, bquota = ?, data_sito = ?, note_sito = ?
							WHERE pkuid = ?;''',  (dict_sito["pkey_sln"], dict_sito["mod_identcoord"],
							dict_sito["desc_modcoord"], dict_sito["Aquota"], dict_sito["Bquota"],
							dict_sito["data_sito"], dict_sito["note_sito"], lastid))
					elif sito_type == "CLE AC":
						cur.execute("INSERT INTO cl_ac (ID_AC, geom) VALUES (?, GeomFromText(?, 32633))", (dict_sito["ID_AC"], geom))
						lastid = cur.lastrowid
						cur.execute('''UPDATE cl_ac SET pkuid = ?, data_ac = ?, regione = ?, cod_reg = ?, provincia = ?, cod_prov = ?,
							comune = ?, cod_com = ?, località = ?, cod_local = ?, tipo_infra = ?, ID_infra = ?, strade_a = ?, strade_b = ?,
							strade_c = ?, strade_d = ?, strade_e = ?, strade_f = ?, largh_max = ?, largh_min = ?, lungh = ?, lungh_vuo = ?,
							pav_per = ?, ost_disc = ?, n_aggreg = ?, n_manuf = ?, el_ferrov = ?, el_pont = ?, el_tunn = ?, el_pont_at = ?,
							el_muri = ?, pendenza = ?, morf = ?, ubic_sotto = ?, ubic_sopra = ?, zona_ms = ?, inst_fran = ?, inst_liq = ?,
							inst_fag = ?, inst_ced = ?, inst_cav = ?, frana_AC = ?, frana_mon = ?, frana_val = ?, falda = ?, acq_sup = ?,
							pai = ?, alluvio = ?, ID_AC = ?
							WHERE pkuid = ?;''',  (dict_sito["data_ac"], dict_sito["regione"], dict_sito["cod_reg"], dict_sito["provincia"],
							dict_sito["cod_prov"], dict_sito["comune"], dict_sito["cod_com"], dict_sito["località"], dict_sito["cod_local"],
							dict_sito["tipo_infra"], dict_sito["ID_infra"], dict_sito["strade_a"], dict_sito["strade_b"], dict_sito["strade_c"],
							dict_sito["strade_d"], dict_sito["strade_e"], dict_sito["strade_f"], dict_sito["largh_max"], dict_sito["largh_min"],
							dict_sito["lungh"], dict_sito["lungh_vuo"], dict_sito["pav_per"], dict_sito["ost_disc"], dict_sito["n_aggreg"],
							dict_sito["n_manuf"], dict_sito["el_ferrov"], dict_sito["el_pont"], dict_sito["el_tunn"], dict_sito["el_pont_at"],
							dict_sito["el_muri"], dict_sito["pendenza"], dict_sito["morf"], dict_sito["ubic_sotto"], dict_sito["ubic_sopra"],
							dict_sito["zona_ms"], dict_sito["inst_fran"], dict_sito["inst_liq"], dict_sito["inst_fag"], dict_sito["inst_ced"],
							dict_sito["inst_cav"], dict_sito["frana_AC"], dict_sito["frana_mon"], dict_sito["frana_val"], dict_sito["falda"],
							dict_sito["acq_sup"], dict_sito["pai"], dict_sito["alluvio"], dict_sito["ID_AC"], lastid))
					elif sito_type == "CLE AE":
						cur.execute("INSERT INTO cl_ae (ID_AE, geom) VALUES (?, GeomFromText(?, 32633))", (dict_sito["ID_AE"], geom))
						lastid = cur.lastrowid
						cur.execute( '''UPDATE cl_ae SET pkuid = ?, data_ae = ?, regione = ?, cod_reg = ?, provincia = ?, cod_prov = ?,
							comune = ?, cod_com = ?, località = ?, cod_local = ?, ID_area = ?, ID_infra_a = ?, ID_infra_b = ?, ID_infra_c = ?,
							ID_infra_d = ?, denom = ?, tipo_area = ?, piano = ?, anno_piano = ?, n_aggreg = ?, n_manuf = ?, superf = ?, rett_max = ?,
							rett_min = ?, pav_per = ?, infra_acq = ?, infra_ele = ?, infra_fog = ?, morf = ?, ubic_sotto = ?, ubic_sopra = ?,
							zona_ms = ?, inst_fran = ?, inst_liq = ?, inst_fag = ?, inst_ced = ?, inst_cav = ?, frana_AE = ?, frana_mon = ?,
							frana_val = ?, falda = ?, acq_sup = ?, pai = ?, alluvio = ?, ID_AE = ?
							WHERE pkuid = ?;''',  (dict_sito["data_ae"], dict_sito["regione"], dict_sito["cod_reg"],
							dict_sito["provincia"], dict_sito["cod_prov"], dict_sito["comune"], dict_sito["cod_com"], dict_sito["località"],
							dict_sito["cod_local"], dict_sito["ID_area"], dict_sito["ID_infra_a"], dict_sito["ID_infra_b"], dict_sito["ID_infra_c"],
							dict_sito["ID_infra_d"], dict_sito["denom"], dict_sito["tipo_area"], dict_sito["piano"], dict_sito["anno_piano"],
							dict_sito["n_aggreg"], dict_sito["n_manuf"], dict_sito["superf"], dict_sito["rett_max"], dict_sito["rett_min"],
							dict_sito["pav_per"], dict_sito["infra_acq"], dict_sito["infra_ele"], dict_sito["infra_fog"], dict_sito["morf"],
							dict_sito["ubic_sotto"], dict_sito["ubic_sopra"], dict_sito["zona_ms"], dict_sito["inst_fran"], dict_sito["inst_liq"],
							dict_sito["inst_fag"], dict_sito["inst_ced"], dict_sito["inst_cav"], dict_sito["frana_AE"], dict_sito["frana_mon"],
							dict_sito["frana_val"], dict_sito["falda"], dict_sito["acq_sup"], dict_sito["pai"], dict_sito["alluvio"], dict_sito["ID_AE"], lastid))
					elif sito_type == "CLE AS":
						cur.execute("INSERT INTO cl_as (ID_AS, geom) VALUES (?, GeomFromText(?, 32633))", (dict_sito["ID_AS"], geom))
						lastid = cur.lastrowid
						cur.execute('''UPDATE cl_as SET pkuid = ?, data_as = ?, regione = ?, cod_reg = ?, provincia = ?, cod_prov = ?, comune = ?,
							cod_com = ?, località = ?, cod_local = ?, sezione = ?, ID_aggr = ?, ID_area = ?, ID_infra_a = ?, ID_infra_b = ?,
							ID_infra_c = ?, ID_infra_d = ?, n_unità = ?, n_edif = ?, n_edif_gl = ?, n_murat = ?, n_ca = ?, n_altre = ?, altezza = ?,
							superf = ?, piani_min = ?, piani_max = ?, lungh_fron = ?, us_interf = ?, conn_volte = ?, conn_rifus = ?, regol_1 = ?,
							regol_2 = ?, regol_3 = ?, regol_4 = ?, regol_5 = ?, vuln_1 = ?, vuln_2 = ?, vuln_3 = ?, vuln_4 = ?, vuln_5 = ?, vuln_6 = ?,
							rinfor_1 = ?, rinfor_2 = ?, morf = ?, ubic_sotto = ?, ubic_sopra = ?, zona_ms = ?, inst_fran = ?, inst_liq = ?, inst_fag = ?,
							inst_ced = ?, inst_cav = ?, frana_AS = ?, frana_mon = ?, frana_val = ?, pai = ?, alluvio = ?, ID_AS = ?
							WHERE pkuid = ?;''',  (dict_sito["data_as"], dict_sito["regione"], dict_sito["cod_reg"],
							dict_sito["provincia"], dict_sito["cod_prov"], dict_sito["comune"], dict_sito["cod_com"], dict_sito["località"], dict_sito["cod_local"],
							dict_sito["sezione"], dict_sito["ID_aggr"], dict_sito["ID_area"], dict_sito["ID_infra_a"], dict_sito["ID_infra_b"],
							dict_sito["ID_infra_c"], dict_sito["ID_infra_d"], dict_sito["n_unità"], dict_sito["n_edif"], dict_sito["n_edif_gl"],
							dict_sito["n_murat"], dict_sito["n_ca"], dict_sito["n_altre"], dict_sito["altezza"], dict_sito["superf"], dict_sito["piani_min"],
							dict_sito["piani_max"], dict_sito["lungh_fron"], dict_sito["us_interf"], dict_sito["conn_volte"], dict_sito["conn_rifus"],
							dict_sito["regol_1"], dict_sito["regol_2"], dict_sito["regol_3"], dict_sito["regol_4"], dict_sito["regol_5"], dict_sito["vuln_1"],
							dict_sito["vuln_2"], dict_sito["vuln_3"], dict_sito["vuln_4"], dict_sito["vuln_5"], dict_sito["vuln_6"], dict_sito["rinfor_1"],
							dict_sito["rinfor_2"], dict_sito["morf"], dict_sito["ubic_sotto"], dict_sito["ubic_sopra"], dict_sito["zona_ms"], dict_sito["inst_fran"],
							dict_sito["inst_liq"], dict_sito["inst_fag"], dict_sito["inst_ced"], dict_sito["inst_cav"], dict_sito["frana_AS"], dict_sito["frana_mon"],
							dict_sito["frana_val"], dict_sito["pai"], dict_sito["alluvio"], dict_sito["ID_AS"], lastid))
					elif sito_type == "CLE ES":
						self.set_log_message.emit(str(dict_sito["ID_ES"]) + "   " + geom)
						cur.execute("INSERT INTO cl_es (ID_ES, geom) VALUES (?, GeomFromText(?, 32633))", (dict_sito["ID_ES"], geom))
						lastid = cur.lastrowid
						cur.execute('''UPDATE cl_es SET pkuid = ?, data_es = ?, regione = ?, cod_reg = ?, provincia = ?, cod_prov = ?, comune = ?, cod_com = ?,
							località = ?, cod_local = ?, sezione = ?, ID_aggr = ?, ID_unit = ?, ID_area = ?, ID_infra_a = ?, ID_infra_b = ?, ID_infra_c = ?,
							ID_infra_d = ?, indirizzo = ?, civico = ?, denom = ?, isolato = ?, posizio = ?, fronte = ?, spec = ?, specialis = ?, n_piani = ?,
							n_interr = ?, alt_piano = ?, alt_totale = ?, vol_unico = ?, superf_m = ?, strutt_ver = ?, tipo_mur = ?, cord_cat = ?, pilastri = ?,
							pilotis = ?, sopraelev = ?, danno = ?, stato_man = ?, pr_pubb = ?, pr_priv = ?, morf = ?, ubic_sotto = ?, ubic_sopra = ?, zona_ms = ?,
							inst_fran = ?, inst_liq = ?, inst_fag = ?, inst_ced = ?, inst_cav = ?, frana_ar = ?, frana_mon = ?, frana_val = ?, pai = ?, alluvio = ?,
							ID_edif = ?, emerg_1 = ?, emerg_2 = ?, emerg_3 = ?, emerg_4 = ?, emerg_5 = ?, emerg_6 = ?, uso_orig = ?, uso_att = ?, anno_prog = ?,
							anno_cost = ?, esp_pers = ?, esp_ore = ?, esp_mes = ?, interv = ?, interv_ann = ?, interv_1 = ?, interv_2 = ?, interv_3 = ?, interv_4 = ?,
							interv_5 = ?, interv_6 = ?, interv_7 = ?, evento_1 = ?, data_ev_1 = ?, tipo_1 = ?, evento_2 = ?, data_ev_2 = ?, tipo_2 = ?, evento_3 = ?,
							data_ev_3 = ?, tipo_3 = ?, verif_sism = ?, ID_ES = ?
							WHERE pkuid = ?;''',  (dict_sito["data_es"], dict_sito["regione"], dict_sito["cod_reg"],
							dict_sito["provincia"], dict_sito["cod_prov"], dict_sito["comune"], dict_sito["cod_com"], dict_sito["località"], dict_sito["cod_local"],
							dict_sito["sezione"], dict_sito["ID_aggr"], dict_sito["ID_unit"], dict_sito["ID_area"], dict_sito["ID_infra_a"], dict_sito["ID_infra_b"],
							dict_sito["ID_infra_c"], dict_sito["ID_infra_d"], dict_sito["indirizzo"], dict_sito["civico"], dict_sito["denom"], dict_sito["isolato"],
							dict_sito["posizio"], dict_sito["fronte"], dict_sito["spec"], dict_sito["specialis"], dict_sito["n_piani"], dict_sito["n_interr"],
							dict_sito["alt_piano"], dict_sito["alt_totale"], dict_sito["vol_unico"], dict_sito["superf_m"], dict_sito["strutt_ver"],
							dict_sito["tipo_mur"], dict_sito["cord_cat"], dict_sito["pilastri"], dict_sito["pilotis"], dict_sito["sopraelev"], dict_sito["danno"],
							dict_sito["stato_man"], dict_sito["pr_pubb"], dict_sito["pr_priv"], dict_sito["morf"], dict_sito["ubic_sotto"], dict_sito["ubic_sopra"],
							dict_sito["zona_ms"], dict_sito["inst_fran"], dict_sito["inst_liq"], dict_sito["inst_fag"], dict_sito["inst_ced"], dict_sito["inst_cav"],
							dict_sito["frana_ar"], dict_sito["frana_mon"], dict_sito["frana_val"], dict_sito["pai"], dict_sito["alluvio"], dict_sito["ID_edif"],
							dict_sito["emerg_1"], dict_sito["emerg_2"], dict_sito["emerg_3"], dict_sito["emerg_4"], dict_sito["emerg_5"], dict_sito["emerg_6"],
							dict_sito["uso_orig"], dict_sito["uso_att"], dict_sito["anno_prog"], dict_sito["anno_cost"], dict_sito["esp_pers"], dict_sito["esp_ore"],
							dict_sito["esp_mes"], dict_sito["interv"], dict_sito["interv_ann"], dict_sito["interv_1"], dict_sito["interv_2"], dict_sito["interv_3"],
							dict_sito["interv_4"], dict_sito["interv_5"], dict_sito["interv_6"], dict_sito["interv_7"], dict_sito["evento_1"], dict_sito["data_ev_1"],
							dict_sito["tipo_1"], dict_sito["evento_2"], dict_sito["data_ev_2"], dict_sito["tipo_2"], dict_sito["evento_3"], dict_sito["data_ev_3"],
							dict_sito["tipo_3"], dict_sito["verif_sism"], dict_sito["ID_ES"], lastid))
					elif sito_type == "CLE US":
						cur.execute("INSERT INTO cl_us (ID_US, geom) VALUES (?, GeomFromText(?, 32633))", (dict_sito["ID_US"], geom))
						lastid = cur.lastrowid
						cur.execute('''UPDATE cl_us SET pkuid = ?, data_us = ?, regione = ?, cod_reg = ?, provincia = ?, cod_prov = ?, comune = ?, cod_com = ?,
							località = ?, cod_local = ?, sezione = ?, ID_aggr = ?, ID_unit = ?, ID_area = ?, ID_infra_a = ?, ID_infra_b = ?, ID_infra_c = ?,
							ID_infra_d = ?, indirizzo = ?, civico = ?, isolato = ?, posizio = ?, fronte = ?, spec = ?, specialis = ?, n_piani = ?, n_interr = ?,
							alt_piano = ?, alt_totale = ?, vol_unico = ?, superf_m = ?, strutt_ver = ?, tipo_mur = ?, cord_cat = ?, pilastri = ?, pilotis = ?,
							sopraelev = ?, danno = ?, stato_man = ?, pr_pubb = ?, pr_priv = ?, morf = ?, ubic_sotto = ?, ubic_sopra = ?, zona_ms = ?, inst_fran = ?,
							inst_liq = ?, inst_fag = ?, inst_ced = ?, inst_cav = ?, frana_ar = ?, frana_mon = ?, frana_val = ?, pai = ?, alluvio = ?, uso_att = ?,
							uso_a = ?, uso_a_1 = ?, uso_b = ?, uso_b_1 = ?, uso_c = ?, uso_c_1 = ?, uso_d = ?, uso_d_1 = ?, uso_e = ?, uso_e_1 = ?, uso_f = ?,
							uso_f_1 = ?, uso_g = ?, uso_g_1 = ?, epoca_1 = ?, epoca_2 = ?, epoca_3 = ?, epoca_4 = ?, epoca_5 = ?, epoca_6 = ?, epoca_7 = ?,
							epoca_8 = ?, utilizz = ?, occupanti = ?, ID_US = ?
							WHERE pkuid = ?;''',  (dict_sito["data_us"], dict_sito["regione"], dict_sito["cod_reg"],
							dict_sito["provincia"], dict_sito["cod_prov"], dict_sito["comune"], dict_sito["cod_com"], dict_sito["località"], dict_sito["cod_local"],
							dict_sito["sezione"], dict_sito["ID_aggr"], dict_sito["ID_unit"], dict_sito["ID_area"], dict_sito["ID_infra_a"], dict_sito["ID_infra_b"],
							dict_sito["ID_infra_c"], dict_sito["ID_infra_d"], dict_sito["indirizzo"], dict_sito["civico"], dict_sito["isolato"], dict_sito["posizio"],
							dict_sito["fronte"], dict_sito["spec"], dict_sito["specialis"], dict_sito["n_piani"], dict_sito["n_interr"], dict_sito["alt_piano"],
							dict_sito["alt_totale"], dict_sito["vol_unico"], dict_sito["superf_m"], dict_sito["strutt_ver"], dict_sito["tipo_mur"],
							dict_sito["cord_cat"], dict_sito["pilastri"], dict_sito["pilotis"], dict_sito["sopraelev"], dict_sito["danno"], dict_sito["stato_man"],
							dict_sito["pr_pubb"], dict_sito["pr_priv"], dict_sito["morf"], dict_sito["ubic_sotto"], dict_sito["ubic_sopra"], dict_sito["zona_ms"],
							dict_sito["inst_fran"], dict_sito["inst_liq"], dict_sito["inst_fag"], dict_sito["inst_ced"], dict_sito["inst_cav"], dict_sito["frana_ar"],
							dict_sito["frana_mon"], dict_sito["frana_val"], dict_sito["pai"], dict_sito["alluvio"], dict_sito["uso_att"], dict_sito["uso_a"],
							dict_sito["uso_a_1"], dict_sito["uso_b"], dict_sito["uso_b_1"], dict_sito["uso_c"], dict_sito["uso_c_1"], dict_sito["uso_d"],
							dict_sito["uso_d_1"], dict_sito["uso_e"], dict_sito["uso_e_1"], dict_sito["uso_f"], dict_sito["uso_f_1"], dict_sito["uso_g"],
							dict_sito["uso_g_1"], dict_sito["epoca_1"], dict_sito["epoca_2"], dict_sito["epoca_3"], dict_sito["epoca_4"], dict_sito["epoca_5"],
							dict_sito["epoca_6"], dict_sito["epoca_7"], dict_sito["epoca_8"], dict_sito["utilizz"], dict_sito["occupanti"], dict_sito["ID_US"], lastid))

					current_feature = current_feature + 1
					if self.killed:
						break

			# restore insert trigger
			# TODO: causes QGIS crash
			# cur.execute(ins_data_s_point if tab_name == "sito_puntuale" else ins_data_s_line)

			conn.commit()

			# check if spatial index needs rebuild
			cur.execute('SELECT RecoverSpatialIndex(?, ?)', (tab_name, 'geom'))
		finally:
			conn.close()

	def insert_table(self, db_table, txt_table):

		# indagini_puntuali
		insert_indpu = """
			INSERT INTO indagini_puntuali
				(pkuid, id_spu, classe_ind, tipo_ind, id_indpu,
				id_indpuex, arch_ex, note_ind, prof_top, prof_bot,
				spessore, quota_slm_top, quota_slm_bot, data_ind,
				doc_pag, doc_ind)
			VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
		select_id_spu = "SELECT pkuid, id_spu FROM sito_puntuale WHERE pkuid = ?"
		update_indpu_fkey = "UPDATE indagini_puntuali SET id_spu = ? WHERE pkuid = ?"

		# parametri_puntuali
		insert_parpu = """
			INSERT INTO parametri_puntuali
				(pkuid, id_indpu, tipo_parpu, id_parpu, prof_top, prof_bot,
				spessore, quota_slm_top, quota_slm_bot, valore, attend_mis,
				tab_curve, note_par, data_par)
			VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
		select_id_indpu = "SELECT pkuid, id_indpu FROM indagini_puntuali WHERE pkuid = ?"
		update_parpu_fkey = "UPDATE parametri_puntuali SET id_indpu = ? WHERE pkuid = ?"

		# curve
		insert_curve = """
			INSERT INTO curve (pkuid, id_parpu, cond_curve, varx, vary)
				VALUES (?,?,?,?,?);"""
		select_id_parpu = "SELECT pkuid, id_parpu FROM parametri_puntuali WHERE pkuid = ?"
		update_curve_fkey = "UPDATE curve SET id_parpu = ? WHERE pkuid = ?"

		# indagini_lineari
		insert_indln = """
			INSERT INTO indagini_lineari
				(pkuid, id_sln, classe_ind, tipo_ind, id_indln, id_indlnex,
				arch_ex, note_indln, data_ind, doc_pag, doc_ind)
			VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
		select_id_sln = "SELECT pkuid, id_sln FROM sito_lineare WHERE pkuid = ?"
		update_indln_fkey = "UPDATE indagini_lineari SET id_sln = ? WHERE pkuid = ?"

		# parametri_lineari
		insert_parln = """
			INSERT INTO parametri_lineari
				(pkuid, id_indln, tipo_parln, id_parln, prof_top, prof_bot,
				spessore, quota_slm_top, quota_slm_bot, valore, attend_mis,
				note_par, data_par)
			VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""
		select_id_indln = "SELECT pkuid, id_indln FROM indagini_lineari WHERE pkuid = ?"
		update_parln_fkey = "UPDATE parametri_lineari SET id_indln = ? WHERE pkuid = ?"

		path_db = self.proj_abs_path + os.sep + "db" + os.sep + "indagini.sqlite"
		conn = sqlite3.connect(path_db)
		conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
		try:
			cur = conn.cursor()
			with open(txt_table,'r') as table:
				dr = csv.DictReader(table, delimiter=';', quotechar='"')
				current_record = 1
				row_num = len(list(dr))
				# restart reading file after line count
				table.seek(0)
				next(dr)
				for i in dr:
					self.set_message.emit("Table %s: inserting record %s/%s" % (db_table, str(current_record), str(row_num)))

					# transform empty strings to None to circumvent db CHECKs
					for k in i:
						if i[k] == "":
							i[k] = None

					if db_table == "indagini_puntuali":
						to_db = (i['pkey_indpu'], i['pkey_spu'], i['classe_ind'], i['tipo_ind'], i['ID_INDPU'], i['id_indpuex'], i['arch_ex'], i['note_ind'], i['prof_top'], i['prof_bot'], i['spessore'], i['quota_slm_top'], i['quota_slm_bot'], i['data_ind'], i['doc_pag'], i['doc_ind'])
						fkey = i['pkey_spu']
						insert_sql = insert_indpu
						select_parent_sql = select_id_spu
						update_sql = update_indpu_fkey
					elif db_table == "parametri_puntuali":
						to_db = (i['pkey_parpu'], i['pkey_indpu'], i['tipo_parpu'], i['ID_PARPU'], i['prof_top'], i['prof_bot'], i['spessore'], i['quota_slm_top'], i['quota_slm_bot'], i['valore'], i['attend_mis'], i['tab_curve'], i['note_par'], i['data_par'])
						fkey = i['pkey_indpu']
						insert_sql = insert_parpu
						select_parent_sql = select_id_indpu
						update_sql = update_parpu_fkey
					elif db_table == "curve":
						to_db = (i['pkey_curve'], i['pkey_parpu'], i['cond_curve'], i['varx'], i['vary'])
						fkey = i['pkey_parpu']
						insert_sql = insert_curve
						select_parent_sql = select_id_parpu
						update_sql = update_curve_fkey
					elif db_table == "indagini_lineari":
						to_db = (i['pkey_indln'], i['pkey_sln'], i['classe_ind'], i['tipo_ind'], i['ID_INDLN'], i['id_indlnex'], i['arch_ex'], i['note_indln'], i['data_ind'], i['doc_pag'], i['doc_ind'])
						fkey = i['pkey_sln']
						insert_sql = insert_indln
						select_parent_sql = select_id_sln
						update_sql = update_indln_fkey
					elif db_table == "parametri_lineari":
						to_db = (i['pkey_parln'], i['pkey_indln'], i['tipo_parln'], i['ID_PARLN'], i['prof_top'], i['prof_bot'], i['spessore'], i['quota_slm_top'], i['quota_slm_bot'], i['valore'], i['attend_mis'], i['note_par'], i['data_par'])
						fkey = i['pkey_indln']
						insert_sql = insert_parln
						select_parent_sql = select_id_indln
						update_sql = update_parln_fkey

					cur.execute(insert_sql, to_db)
					id_last_insert = cur.lastrowid
					cur.execute(select_parent_sql, (fkey,))
					id_parent = cur.fetchone()[1]
					cur.execute(update_sql, (id_parent, id_last_insert))

					current_record = current_record + 1
					if self.killed:
						break

			conn.commit()
		finally:
			conn.close()

	def calc_join(self, orig_tab, link_tab, temp_field, link_field, orig_field):

		path_db = self.proj_abs_path + os.sep + "db" + os.sep + "indagini.sqlite"

		joinObject = QgsVectorJoinInfo()
		joinObject.joinLayerId = link_tab.id()
		joinObject.joinFieldName = 'pkuid'
		joinObject.targetFieldName = temp_field
		joinObject.memoryCache = True
		orig_tab.addJoin(joinObject)

		context = QgsExpressionContext()
		scope = QgsExpressionContextScope()
		context.appendScope(scope)

		expression = QgsExpression(link_field)
		expression.prepare(orig_tab.pendingFields())

		try:
			conn = sqlite3.connect(path_db)
			conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
			cur = conn.cursor()

			for feature in orig_tab.getFeatures():
				scope.setFeature(feature)
				value = expression.evaluate(context)
				if value is None:
					pass
				else:
					nome_tab = LAYER_DB_TAB[orig_tab.name()]
#					 cur.execute("UPDATE %s SET %s  = %s WHERE pkuid = %s;" % nome_tab, orig_field, value, str(feature['pkuid']))
					cur.execute("UPDATE ? SET ?  = ? WHERE pkuid = ?", (nome_tab, orig_field, value, str(feature['pkuid'])))

			conn.commit()
		except Exception as ex:
			# error will be forwarded upstream
			raise ex
		finally:
			conn.close()

		orig_tab.removeJoin(link_tab.id())

	def copy_files(self, src, dest):
		for file_name in os.listdir(src):
			full_file_name = os.path.join(src, file_name)
			if (os.path.isfile(full_file_name)):
				shutil.copy(full_file_name, dest)