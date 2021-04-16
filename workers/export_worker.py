# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:		export_workers.py
# Author:   Tarquini E.
# Created:	 18-03-2019
# -------------------------------------------------------------------------------

import os
import shutil
import sqlite3
import sys
import webbrowser
import zipfile

from ..constants import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt import uic
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.utils import *

from .abstract_worker import AbstractWorker, UserAbortedNotification


class ExportWorker(AbstractWorker):
    '''Worker class handling data import from existing project'''

    def __init__(self, in_dir, out_dir, plugin_dir):
        AbstractWorker.__init__(self)
#		 self.steps = steps
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.plugin_dir = plugin_dir

        self.current_step = 1

    def work(self):
        # calculate steps
        total_steps = len(POSIZIONE) + 4

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
			epoca_4,epoca_5,epoca_6,epoca_7,epoca_8,utilizz,occupanti,ID_US FROM A.cl_us;""",
                           """INSERT INTO 'metadati'(id_metadato, liv_gerarchico, resp_metadato_nome, resp_metadato_email, resp_metadato_sito, data_metadato, srs_dati, proprieta_dato_nome, proprieta_dato_email,
			proprieta_dato_sito, data_dato, ruolo, desc_dato, formato, tipo_dato, contatto_dato_nome, contatto_dato_email, contatto_dato_sito, keywords, keywords_inspire, limitazione, vincoli_accesso,
			vincoli_fruibilita, vincoli_sicurezza, scala, categoria_iso, estensione_ovest, estensione_est, estensione_sud, estensione_nord, formato_dati, distributore_dato_nome, distributore_dato_telefono,
			distributore_dato_email, distributore_dato_sito, url_accesso_dato, funzione_accesso_dato, precisione, genealogia) SELECT id_metadato, liv_gerarchico, resp_metadato_nome, resp_metadato_email,
			resp_metadato_sito, data_metadato, srs_dati, proprieta_dato_nome, proprieta_dato_email, proprieta_dato_sito, data_dato, ruolo, desc_dato, formato, tipo_dato, contatto_dato_nome, contatto_dato_email,
			contatto_dato_sito, keywords, keywords_inspire, limitazione, vincoli_accesso, vincoli_fruibilita, vincoli_sicurezza, scala, categoria_iso, estensione_ovest, estensione_est, estensione_sud,
			estensione_nord, formato_dati, distributore_dato_nome, distributore_dato_telefono, distributore_dato_email, distributore_dato_sito, url_accesso_dato, funzione_accesso_dato, precisione,
			genealogia FROM A.metadati;"""]

        # step 1 (preparing data)
        ###############################################
        self.set_message.emit('Creating project...')
        self.set_log_message.emit('Creating project...\n')
        input_name = self.out_dir + os.sep + "progetto_shapefile"
        output_name = self.out_dir + os.sep + self.in_dir.split("/")[-1]
        zip_ref = zipfile.ZipFile(
            self.plugin_dir + os.sep + "data" + os.sep + "progetto_shapefile.zip", 'r')
        zip_ref.extractall(self.out_dir)
        zip_ref.close()
        os.rename(input_name, output_name)
        self.set_log_message.emit('Done!\n')

        self.current_step = self.current_step + 1
        self.progress.emit(self.current_step * 100/total_steps)

        # step 2 (inserting features)
        ###############################################
        self.set_message.emit('Creating shapefiles:')
        self.set_log_message.emit('\nCreating shapefiles:\n')

        for chiave, valore in POSIZIONE.items():
            sourceLYR = QgsProject.instance().mapLayersByName(chiave)[0]
            QgsVectorFileWriter.writeAsVectorFormat(
                sourceLYR, output_name + os.sep + valore[0] + os.sep + valore[1], "utf-8", None, "ESRI Shapefile")
            selected_layer = QgsVectorLayer(
                output_name + os.sep + valore[0] + os.sep + valore[1] + ".shp", valore[1], 'ogr')
            if chiave == "Infrastrutture di accessibilita'/connessione" or chiave == "Aree di emergenza" or chiave == "Aggregati strutturali" or chiave == "Edifici strategici" or chiave == "Unita' strutturali":
                self.esporta([0, ["cod_prov", "cod_com", "ID_aggr", "ID_unit", "ID_ES",
                                  "ID_area", "ID_AE", "ID_infra", "ID_AC", "ID_AS", "ID_US"]], selected_layer)
                self.set_message.emit(
                    "'" + chiave + "' shapefile has been created!")
                self.set_log_message.emit(
                    "  '" + chiave + "' shapefile has been created!\n")
            else:
                self.esporta([1, ['pkuid']], selected_layer)
                self.set_message.emit(
                    "'" + chiave + "' shapefile has been created!")
                self.set_log_message.emit(
                    "  '" + chiave + "' shapefile has been created!\n")

            if self.killed:
                break

            self.current_step = self.current_step + 1
            self.progress.emit(self.current_step * 100/total_steps)

        # end for
        if self.killed:
            raise UserAbortedNotification('USER Killed')

        # step 3 (miscellaneous files)
        #######################################################
        self.set_message.emit('Adding miscellaneous files...')
        self.set_log_message.emit('\nAdding miscellaneous files...\n')

        if os.path.exists(self.in_dir + os.sep + "allegati" + os.sep + "Plot"):
            self.set_message.emit("Copying 'Plot' folder")
            self.set_log_message.emit("  Copying 'Plot' folder\n")
            shutil.copytree(self.in_dir + os.sep + "allegati" +
                            os.sep + "Plot", output_name + os.sep + "Plot")
        if os.path.exists(self.in_dir + os.sep + "allegati" + os.sep + "altro"):
            self.set_message.emit("Copying 'altro' folder")
            self.set_log_message.emit("  Copying 'altro' folder\n")
            shutil.copytree(self.in_dir + os.sep + "allegati" +
                            os.sep + "altro", output_name + os.sep + "altro")

        self.current_step = self.current_step + 1
        self.progress.emit(self.current_step * 100/total_steps)

        for file_name in os.listdir(self.in_dir + os.sep + "allegati"):
            if file_name.endswith(".txt"):
                shutil.copyfile(self.in_dir + os.sep + "allegati" +
                                os.sep + file_name, output_name + os.sep + file_name)

        self.set_message.emit("Creating 'CLE_db.sqlite'")
        self.set_log_message.emit("\nCreating 'CLE_db.sqlite'\n")
        dir_gdb_cle = output_name + os.sep + "CLE" + os.sep + "CLE_db.sqlite"
        orig_gdb = self.in_dir + os.sep + "db" + os.sep + "indagini.sqlite"
        conn = sqlite3.connect(dir_gdb_cle)
        sql = """ATTACH '""" + orig_gdb + """' AS A;"""
        conn.execute(sql)
        for query in LISTA_QUERY_CLE:
            conn.execute(query)
            conn.commit()
        conn.close()

        self.set_log_message.emit("Done!")
        self.current_step = self.current_step + 1
        self.progress.emit(self.current_step * 100/total_steps)

        return 'Export completed!'

    def esporta(self, list_attr, selected_layer):

        field_ids = []
        fieldnames = set(list_attr[1])
        if list_attr[0] == 0:
            for field in selected_layer.fields():
                if field.name() not in fieldnames:
                    field_ids.append(
                        selected_layer.fieldNameIndex(field.name()))
            selected_layer.dataProvider().deleteAttributes(field_ids)
            selected_layer.updateFields()
        elif list_attr[0] == 1:
            for field in selected_layer.fields():
                if field.name() in fieldnames:
                    field_ids.append(
                        selected_layer.fieldNameIndex(field.name()))
            selected_layer.dataProvider().deleteAttributes(field_ids)
            selected_layer.updateFields()
