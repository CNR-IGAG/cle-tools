import os
from string import Template

from qgis.core import QgsProject
from qgis.PyQt.QtGui import QTextDocument
from qgis.PyQt.QtPrintSupport import QPrinter

from .abstract_worker import AbstractWorker, UserAbortedNotification


class ReportWorker(AbstractWorker):
    """Worker class handling report generation"""

    def __init__(self, out_dir):
        super().__init__()
        self.out_dir = out_dir
        self.current_step = 1

        # setup QPrinter
        self.printer = QPrinter()
        self.printer.setPageSize(QPrinter.A4)
        self.printer.setFullPage(True)
        self.printer.setOutputFormat(QPrinter.PdfFormat)

        templates_path = os.path.join(os.path.dirname(__file__), "report_templates")

        # load templates
        with open(os.path.join(templates_path, "infrastrutture_tmpl.html"), "r") as f:
            self.infrastrutture_tmpl = Template(f.read())
        with open(os.path.join(templates_path, "aree_emerg_tmpl.html"), "r") as f:
            self.aree_emerg_tmpl = Template(f.read())
        with open(os.path.join(templates_path, "aggregati_tmpl.html"), "r") as f:
            self.aggregati_tmpl = Template(f.read())
        with open(os.path.join(templates_path, "edifici_tmpl.html"), "r") as f:
            self.edifici_tmpl = Template(f.read())
        with open(os.path.join(templates_path, "unita_strutt_tmpl.html"), "r") as f:
            self.unita_strutt_tmpl = Template(f.read())

        # load lookup tables
        self.tipo_infra_dict = self._gen_codes_dict("vw_tipo_infra")
        self.pav_per_dict = self._gen_codes_dict("vw_pav_per")
        self.ost_disc_dict = self._gen_codes_dict("vw_ost_disc")
        self.morf_dict = self._gen_codes_dict("vw_morf")
        self.zona_ms_dict = self._gen_codes_dict("vw_zona_ms")
        self.falda_dict = self._gen_codes_dict("vw_falda")
        self.acq_sup_dict = self._gen_codes_dict("vw_acq_sup")
        self.pai_dict = self._gen_codes_dict("vw_pai")
        self.tipo_area_dict = self._gen_codes_dict("vw_tipo_area")
        self.piano_dict = self._gen_codes_dict("vw_piano")
        self.infra_acq_dict = self._gen_codes_dict("vw_infra_acq")
        self.infra_ele_dict = self._gen_codes_dict("vw_infra_ele")
        self.infra_fog_dict = self._gen_codes_dict("vw_infra_fog")
        self.posizio_dict = self._gen_codes_dict("vw_posizio")
        self.specialis_dict = self._gen_codes_dict("vw_specialis")
        self.n_interr_dict = self._gen_codes_dict("vw_n_interr")
        self.alt_piano_dict = self._gen_codes_dict("vw_alt_piano")
        self.strutt_ver_dict = self._gen_codes_dict("vw_strutt_ver")
        self.tipo_mur_dict = self._gen_codes_dict("vw_tipo_mur")
        self.danno_dict = self._gen_codes_dict("vw_danno")
        self.stato_man_dict = self._gen_codes_dict("vw_stato_man")
        self.id_edif_dict = self._gen_codes_dict("vw_id_edif")
        self.uso_att_dict = self._gen_codes_dict("vw_uso_att")
        self.evento_dict = self._gen_codes_dict("vw_evento")
        self.tipo_evento_dict = self._gen_codes_dict("vw_tipo")
        self.verif_sism_dict = self._gen_codes_dict("vw_verif_sism")
        self.utilizz_dict = self._gen_codes_dict("vw_utilizz")

    def _gen_codes_dict(self, lookup_table_name):
        """Generate dictionary with codes from lookup table"""
        lookup_table = QgsProject.instance().mapLayersByName(lookup_table_name)[0]
        dict = {}
        for f in lookup_table.getFeatures():
            dict[f["cod"]] = f["descrizione"]
        return dict

    def work(self):
        root = QgsProject.instance().layerTreeRoot()
        cle_group = root.findGroup("CLE")
        cle_layer_nodes = cle_group.children()

        for node in cle_layer_nodes:
            self.set_message.emit(f"Generating reports for {node.layer().name()}...")
            features = node.layer().getFeatures()
            cnt = 0

            for feature in features:
                self.generate_report(node.layer().name(), feature)
                cnt += 1
                self.progress.emit(int(cnt * 100 / node.layer().featureCount()))

                if self.killed:
                    break

            if self.killed:
                raise UserAbortedNotification("User aborted")

        return "Task completed!"

    def generate_report(self, layer_name, feature):
        # self.set_message.emit(f'Generating report for {feature["ID_AC"]} ({layer_name})')

        # dictionary with field names and values of the feature
        attrs_dict = dict(zip(feature.fields().names(), feature.attributes()))

        html = None

        if layer_name.startswith("Infrastrutture"):
            pdf_name = f"{feature['ID_AC']}.pdf"
            if not os.path.exists(os.path.join(self.out_dir, "Infrastrutture")):
                os.mkdir(os.path.join(self.out_dir, "Infrastrutture"))
            pdf_path = os.path.join(self.out_dir, "Infrastrutture", pdf_name)
            self.printer.setOutputFileName(pdf_path)

            # substitute codes with corresponding values from lookup tables
            attrs_dict["tipo_infra"] = self.tipo_infra_dict[attrs_dict["tipo_infra"]]
            attrs_dict["strade_a"] = "&#9745;" if attrs_dict["strade_a"] == "true" else "&#9744;"
            attrs_dict["strade_b"] = "&#9745;" if attrs_dict["strade_b"] == "true" else "&#9744;"
            attrs_dict["strade_c"] = "&#9745;" if attrs_dict["strade_c"] == "true" else "&#9744;"
            attrs_dict["strade_d"] = "&#9745;" if attrs_dict["strade_d"] == "true" else "&#9744;"
            attrs_dict["strade_e"] = "&#9745;" if attrs_dict["strade_e"] == "true" else "&#9744;"
            attrs_dict["strade_f"] = "&#9745;" if attrs_dict["strade_f"] == "true" else "&#9744;"
            attrs_dict["pav_per"] = self.pav_per_dict[attrs_dict["pav_per"]]
            attrs_dict["ost_disc"] = self.ost_disc_dict[attrs_dict["ost_disc"]]
            attrs_dict["morf"] = self.morf_dict[attrs_dict["morf"]]
            attrs_dict["ubic_sotto"] = "&#9745;" if attrs_dict["ubic_sotto"] == "true" else "&#9744;"
            attrs_dict["ubic_sopra"] = "&#9745;" if attrs_dict["ubic_sopra"] == "true" else "&#9744;"
            attrs_dict["zona_ms"] = self.zona_ms_dict[attrs_dict["zona_ms"]]
            attrs_dict["inst_fran"] = "&#9745;" if attrs_dict["inst_fran"] == "true" else "&#9744;"
            attrs_dict["inst_liq"] = "&#9745;" if attrs_dict["inst_liq"] == "true" else "&#9744;"
            attrs_dict["inst_fag"] = "&#9745;" if attrs_dict["inst_fag"] == "true" else "&#9744;"
            attrs_dict["inst_ced"] = "&#9745;" if attrs_dict["inst_ced"] == "true" else "&#9744;"
            attrs_dict["inst_cav"] = "&#9745;" if attrs_dict["inst_cav"] == "true" else "&#9744;"
            attrs_dict["frana_AC"] = "&#9745;" if attrs_dict["frana_AC"] == "true" else "&#9744;"
            attrs_dict["frana_mon"] = "&#9745;" if attrs_dict["frana_mon"] == "true" else "&#9744;"
            attrs_dict["frana_val"] = "&#9745;" if attrs_dict["frana_val"] == "true" else "&#9744;"
            attrs_dict["falda"] = self.falda_dict[attrs_dict["falda"]]
            attrs_dict["acq_sup"] = self.acq_sup_dict[attrs_dict["acq_sup"]]
            attrs_dict["pai"] = self.pai_dict[attrs_dict["pai"]]
            attrs_dict["alluvio"] = "&#9745;" if attrs_dict["alluvio"] == "true" else "&#9744;"

            html = self.infrastrutture_tmpl.substitute(attrs_dict)

        elif layer_name.startswith("Aree"):
            pdf_name = f"{feature['ID_AE']}.pdf"
            if not os.path.exists(os.path.join(self.out_dir, "Aree_emergenza")):
                os.mkdir(os.path.join(self.out_dir, "Aree_emergenza"))
            pdf_path = os.path.join(self.out_dir, "Aree_emergenza", pdf_name)
            self.printer.setOutputFileName(pdf_path)

            # substitute codes with corresponding values from lookup tables
            attrs_dict["tipo_area"] = self.tipo_area_dict[attrs_dict["tipo_area"]]
            attrs_dict["piano"] = self.piano_dict[attrs_dict["piano"]]
            attrs_dict["pav_per"] = self.pav_per_dict[attrs_dict["pav_per"]]
            attrs_dict["infra_acq"] = self.infra_acq_dict[attrs_dict["infra_acq"]]
            attrs_dict["infra_ele"] = self.infra_ele_dict[attrs_dict["infra_ele"]]
            attrs_dict["infra_fog"] = self.infra_fog_dict[attrs_dict["infra_fog"]]
            attrs_dict["morf"] = self.morf_dict[attrs_dict["morf"]]
            attrs_dict["ubic_sotto"] = "&#9745;" if attrs_dict["ubic_sotto"] == "true" else "&#9744;"
            attrs_dict["ubic_sopra"] = "&#9745;" if attrs_dict["ubic_sopra"] == "true" else "&#9744;"
            attrs_dict["zona_ms"] = self.zona_ms_dict[attrs_dict["zona_ms"]]
            attrs_dict["inst_fran"] = "&#9745;" if attrs_dict["inst_fran"] == "true" else "&#9744;"
            attrs_dict["inst_liq"] = "&#9745;" if attrs_dict["inst_liq"] == "true" else "&#9744;"
            attrs_dict["inst_fag"] = "&#9745;" if attrs_dict["inst_fag"] == "true" else "&#9744;"
            attrs_dict["inst_ced"] = "&#9745;" if attrs_dict["inst_ced"] == "true" else "&#9744;"
            attrs_dict["inst_cav"] = "&#9745;" if attrs_dict["inst_cav"] == "true" else "&#9744;"
            attrs_dict["frana_AE"] = "&#9745;" if attrs_dict["frana_AE"] == "true" else "&#9744;"
            attrs_dict["frana_mon"] = "&#9745;" if attrs_dict["frana_mon"] == "true" else "&#9744;"
            attrs_dict["frana_val"] = "&#9745;" if attrs_dict["frana_val"] == "true" else "&#9744;"
            attrs_dict["falda"] = self.falda_dict[attrs_dict["falda"]]
            attrs_dict["acq_sup"] = self.acq_sup_dict[attrs_dict["acq_sup"]]
            attrs_dict["pai"] = self.pai_dict[attrs_dict["pai"]]
            attrs_dict["alluvio"] = "&#9745;" if attrs_dict["alluvio"] == "true" else "&#9744;"

            html = self.aree_emerg_tmpl.substitute(attrs_dict)

        elif layer_name.startswith("Aggregati"):
            pdf_name = f"{feature['ID_AS']}.pdf"
            if not os.path.exists(os.path.join(self.out_dir, "Aggregati_strutturali")):
                os.mkdir(os.path.join(self.out_dir, "Aggregati_strutturali"))
            pdf_path = os.path.join(self.out_dir, "Aggregati_strutturali", pdf_name)
            self.printer.setOutputFileName(pdf_path)

            # substitute codes with corresponding values from lookup tables
            attrs_dict["conn_volte"] = "&#9745;" if attrs_dict["conn_volte"] == "true" else "&#9744;"
            attrs_dict["conn_rifus"] = "&#9745;" if attrs_dict["conn_rifus"] == "true" else "&#9744;"
            attrs_dict["regol_1"] = "&#9745;" if attrs_dict["regol_1"] == "true" else "&#9744;"
            attrs_dict["regol_2"] = "&#9745;" if attrs_dict["regol_2"] == "true" else "&#9744;"
            attrs_dict["regol_3"] = "&#9745;" if attrs_dict["regol_3"] == "true" else "&#9744;"
            attrs_dict["regol_4"] = "&#9745;" if attrs_dict["regol_4"] == "true" else "&#9744;"
            attrs_dict["regol_5"] = "&#9745;" if attrs_dict["regol_5"] == "true" else "&#9744;"
            attrs_dict["vuln_1"] = "&#9745;" if attrs_dict["vuln_1"] == "true" else "&#9744;"
            attrs_dict["vuln_2"] = "&#9745;" if attrs_dict["vuln_2"] == "true" else "&#9744;"
            attrs_dict["vuln_3"] = "&#9745;" if attrs_dict["vuln_3"] == "true" else "&#9744;"
            attrs_dict["vuln_4"] = "&#9745;" if attrs_dict["vuln_4"] == "true" else "&#9744;"
            attrs_dict["vuln_5"] = "&#9745;" if attrs_dict["vuln_5"] == "true" else "&#9744;"
            attrs_dict["vuln_6"] = "&#9745;" if attrs_dict["vuln_6"] == "true" else "&#9744;"
            attrs_dict["rinfor_1"] = "&#9745;" if attrs_dict["rinfor_1"] == "true" else "&#9744;"
            attrs_dict["rinfor_2"] = "&#9745;" if attrs_dict["rinfor_2"] == "true" else "&#9744;"
            attrs_dict["morf"] = self.morf_dict[attrs_dict["morf"]]
            attrs_dict["ubic_sotto"] = "&#9745;" if attrs_dict["ubic_sotto"] == "true" else "&#9744;"
            attrs_dict["ubic_sopra"] = "&#9745;" if attrs_dict["ubic_sopra"] == "true" else "&#9744;"
            attrs_dict["zona_ms"] = self.zona_ms_dict[attrs_dict["zona_ms"]]
            attrs_dict["inst_fran"] = "&#9745;" if attrs_dict["inst_fran"] == "true" else "&#9744;"
            attrs_dict["inst_liq"] = "&#9745;" if attrs_dict["inst_liq"] == "true" else "&#9744;"
            attrs_dict["inst_fag"] = "&#9745;" if attrs_dict["inst_fag"] == "true" else "&#9744;"
            attrs_dict["inst_ced"] = "&#9745;" if attrs_dict["inst_ced"] == "true" else "&#9744;"
            attrs_dict["inst_cav"] = "&#9745;" if attrs_dict["inst_cav"] == "true" else "&#9744;"
            attrs_dict["frana_AS"] = "&#9745;" if attrs_dict["frana_AS"] == "true" else "&#9744;"
            attrs_dict["frana_mon"] = "&#9745;" if attrs_dict["frana_mon"] == "true" else "&#9744;"
            attrs_dict["frana_val"] = "&#9745;" if attrs_dict["frana_val"] == "true" else "&#9744;"
            attrs_dict["pai"] = self.pai_dict[attrs_dict["pai"]]
            attrs_dict["alluvio"] = "&#9745;" if attrs_dict["alluvio"] == "true" else "&#9744;"

            html = self.aggregati_tmpl.substitute(attrs_dict)

        elif layer_name.startswith("Edifici"):
            pdf_name = f"{feature['ID_ES']}.pdf"
            if not os.path.exists(os.path.join(self.out_dir, "Edifici_strategici")):
                os.mkdir(os.path.join(self.out_dir, "Edifici_strategici"))
            pdf_path = os.path.join(self.out_dir, "Edifici_strategici", pdf_name)
            self.printer.setOutputFileName(pdf_path)

            # substitute codes with corresponding values from lookup tables
            attrs_dict["isolato"] = "&#9745;" if attrs_dict["isolato"] == "true" else "&#9744;"
            attrs_dict["posizio"] = self.posizio_dict[attrs_dict["posizio"]]
            attrs_dict["fronte"] = "&#9745;" if attrs_dict["fronte"] == "true" else "&#9744;"
            attrs_dict["specialis"] = self.specialis_dict[attrs_dict["specialis"]] if attrs_dict["spec"] == "true" else ""
            attrs_dict["spec"] = "&#9745;" if attrs_dict["spec"] == "true" else "&#9744;"
            attrs_dict["n_interr"] = self.n_interr_dict[attrs_dict["n_interr"]]
            attrs_dict["alt_piano"] = self.alt_piano_dict[attrs_dict["alt_piano"]]
            attrs_dict["vol_unico"] = "&#9745;" if attrs_dict["vol_unico"] == "true" else "&#9744;"
            attrs_dict["strutt_ver"] = self.strutt_ver_dict[attrs_dict["strutt_ver"]]
            attrs_dict["tipo_mur"] = self.tipo_mur_dict[attrs_dict["tipo_mur"]]
            attrs_dict["cord_cat"] = "&#9745;" if attrs_dict["cord_cat"] == "true" else "&#9744;"
            attrs_dict["pilastri"] = "&#9745;" if attrs_dict["pilastri"] == "true" else "&#9744;"
            attrs_dict["pilotis"] = "&#9745;" if attrs_dict["pilotis"] == "true" else "&#9744;"
            attrs_dict["sopraelev"] = "&#9745;" if attrs_dict["sopraelev"] == "true" else "&#9744;"
            attrs_dict["danno"] = self.danno_dict[attrs_dict["danno"]]
            attrs_dict["stato_man"] = self.stato_man_dict[attrs_dict["stato_man"]]
            attrs_dict["pr_pubb"] = "&#9745;" if attrs_dict["pr_pubb"] == "true" else "&#9744;"
            attrs_dict["pr_priv"] = "&#9745;" if attrs_dict["pr_priv"] == "true" else "&#9744;"
            attrs_dict["morf"] = self.morf_dict[attrs_dict["morf"]]
            attrs_dict["ubic_sotto"] = "&#9745;" if attrs_dict["ubic_sotto"] == "true" else "&#9744;"
            attrs_dict["ubic_sopra"] = "&#9745;" if attrs_dict["ubic_sopra"] == "true" else "&#9744;"
            attrs_dict["zona_ms"] = self.zona_ms_dict[attrs_dict["zona_ms"]]
            attrs_dict["inst_fran"] = "&#9745;" if attrs_dict["inst_fran"] == "true" else "&#9744;"
            attrs_dict["inst_liq"] = "&#9745;" if attrs_dict["inst_liq"] == "true" else "&#9744;"
            attrs_dict["inst_fag"] = "&#9745;" if attrs_dict["inst_fag"] == "true" else "&#9744;"
            attrs_dict["inst_ced"] = "&#9745;" if attrs_dict["inst_ced"] == "true" else "&#9744;"
            attrs_dict["inst_cav"] = "&#9745;" if attrs_dict["inst_cav"] == "true" else "&#9744;"
            attrs_dict["frana_ar"] = "&#9745;" if attrs_dict["frana_ar"] == "true" else "&#9744;"
            attrs_dict["frana_mon"] = "&#9745;" if attrs_dict["frana_mon"] == "true" else "&#9744;"
            attrs_dict["frana_val"] = "&#9745;" if attrs_dict["frana_val"] == "true" else "&#9744;"
            attrs_dict["pai"] = self.pai_dict[attrs_dict["pai"]]
            attrs_dict["alluvio"] = "&#9745;" if attrs_dict["alluvio"] == "true" else "&#9744;"
            attrs_dict["ID_edif"] = self.id_edif_dict[attrs_dict["ID_edif"]]
            attrs_dict["emerg_1"] = "&#9745;" if attrs_dict["emerg_1"] == "true" else "&#9744;"
            attrs_dict["emerg_2"] = "&#9745;" if attrs_dict["emerg_2"] == "true" else "&#9744;"
            attrs_dict["emerg_3"] = "&#9745;" if attrs_dict["emerg_3"] == "true" else "&#9744;"
            attrs_dict["emerg_4"] = "&#9745;" if attrs_dict["emerg_4"] == "true" else "&#9744;"
            attrs_dict["emerg_5"] = "&#9745;" if attrs_dict["emerg_5"] == "true" else "&#9744;"
            attrs_dict["emerg_6"] = "&#9745;" if attrs_dict["emerg_6"] == "true" else "&#9744;"
            attrs_dict["uso_orig"] = self.uso_att_dict[attrs_dict["uso_orig"]]
            attrs_dict["uso_att"] = self.uso_att_dict[attrs_dict["uso_att"]]
            attrs_dict["interv"] = "&#9745;" if attrs_dict["interv"] == "true" else "&#9744;"
            attrs_dict["interv_1"] = "&#9745;" if attrs_dict["interv_1"] == "true" else "&#9744;"
            attrs_dict["interv_2"] = "&#9745;" if attrs_dict["interv_2"] == "true" else "&#9744;"
            attrs_dict["interv_3"] = "&#9745;" if attrs_dict["interv_3"] == "true" else "&#9744;"
            attrs_dict["interv_4"] = "&#9745;" if attrs_dict["interv_4"] == "true" else "&#9744;"
            attrs_dict["interv_5"] = "&#9745;" if attrs_dict["interv_5"] == "true" else "&#9744;"
            attrs_dict["interv_6"] = "&#9745;" if attrs_dict["interv_6"] == "true" else "&#9744;"
            attrs_dict["interv_7"] = "&#9745;" if attrs_dict["interv_7"] == "true" else "&#9744;"
            attrs_dict["evento_1"] = self.evento_dict[attrs_dict["evento_1"]] if attrs_dict["evento_1"] else ""
            attrs_dict["data_ev_1"] = attrs_dict["data_ev_1"] if attrs_dict["evento_1"] else ""
            attrs_dict["tipo_1"] = self.tipo_evento_dict[attrs_dict["tipo_1"]] if attrs_dict["evento_1"] else ""
            attrs_dict["evento_2"] = self.evento_dict[attrs_dict["evento_2"]] if attrs_dict["evento_2"] else ""
            attrs_dict["data_ev_2"] = attrs_dict["data_ev_2"] if attrs_dict["evento_2"] else ""
            attrs_dict["tipo_2"] = self.tipo_evento_dict[attrs_dict["tipo_2"]] if attrs_dict["evento_2"] else ""
            attrs_dict["evento_3"] = self.evento_dict[attrs_dict["evento_3"]] if attrs_dict["evento_3"] else ""
            attrs_dict["data_ev_3"] = attrs_dict["data_ev_3"] if attrs_dict["evento_3"] else ""
            attrs_dict["tipo_3"] = self.tipo_evento_dict[attrs_dict["tipo_3"]] if attrs_dict["evento_3"] else ""
            attrs_dict["verif_sism"] = self.verif_sism_dict[attrs_dict["verif_sism"]]

            html = self.edifici_tmpl.substitute(attrs_dict)

        elif layer_name.startswith("Unita"):
            pdf_name = f"{feature['ID_US']}.pdf"
            if not os.path.exists(os.path.join(self.out_dir, "Unita_strutturali")):
                os.mkdir(os.path.join(self.out_dir, "Unita_strutturali"))
            pdf_path = os.path.join(self.out_dir, "Unita_strutturali", pdf_name)
            self.printer.setOutputFileName(pdf_path)

            # substitute codes with corresponding values from lookup tables
            attrs_dict["isolato"] = "&#9745;" if attrs_dict["isolato"] == "true" else "&#9744;"
            attrs_dict["posizio"] = self.posizio_dict[attrs_dict["posizio"]]
            attrs_dict["fronte"] = "&#9745;" if attrs_dict["fronte"] == "true" else "&#9744;"
            attrs_dict["specialis"] = self.specialis_dict[attrs_dict["specialis"]] if attrs_dict["spec"] == "true" else ""
            attrs_dict["spec"] = "&#9745;" if attrs_dict["spec"] == "true" else "&#9744;"
            attrs_dict["n_interr"] = self.n_interr_dict[attrs_dict["n_interr"]]
            attrs_dict["alt_piano"] = self.alt_piano_dict[attrs_dict["alt_piano"]]
            attrs_dict["vol_unico"] = "&#9745;" if attrs_dict["vol_unico"] == "true" else "&#9744;"
            attrs_dict["strutt_ver"] = self.strutt_ver_dict[attrs_dict["strutt_ver"]]
            attrs_dict["tipo_mur"] = self.tipo_mur_dict[attrs_dict["tipo_mur"]]
            attrs_dict["cord_cat"] = "&#9745;" if attrs_dict["cord_cat"] == "true" else "&#9744;"
            attrs_dict["pilastri"] = "&#9745;" if attrs_dict["pilastri"] == "true" else "&#9744;"
            attrs_dict["pilotis"] = "&#9745;" if attrs_dict["pilotis"] == "true" else "&#9744;"
            attrs_dict["sopraelev"] = "&#9745;" if attrs_dict["sopraelev"] == "true" else "&#9744;"
            attrs_dict["danno"] = self.danno_dict[attrs_dict["danno"]]
            attrs_dict["stato_man"] = self.stato_man_dict[attrs_dict["stato_man"]]
            attrs_dict["pr_pubb"] = "&#9745;" if attrs_dict["pr_pubb"] == "true" else "&#9744;"
            attrs_dict["pr_priv"] = "&#9745;" if attrs_dict["pr_priv"] == "true" else "&#9744;"
            attrs_dict["morf"] = self.morf_dict[attrs_dict["morf"]]
            attrs_dict["ubic_sotto"] = "&#9745;" if attrs_dict["ubic_sotto"] == "true" else "&#9744;"
            attrs_dict["ubic_sopra"] = "&#9745;" if attrs_dict["ubic_sopra"] == "true" else "&#9744;"
            attrs_dict["zona_ms"] = self.zona_ms_dict[attrs_dict["zona_ms"]]
            attrs_dict["inst_fran"] = "&#9745;" if attrs_dict["inst_fran"] == "true" else "&#9744;"
            attrs_dict["inst_liq"] = "&#9745;" if attrs_dict["inst_liq"] == "true" else "&#9744;"
            attrs_dict["inst_fag"] = "&#9745;" if attrs_dict["inst_fag"] == "true" else "&#9744;"
            attrs_dict["inst_ced"] = "&#9745;" if attrs_dict["inst_ced"] == "true" else "&#9744;"
            attrs_dict["inst_cav"] = "&#9745;" if attrs_dict["inst_cav"] == "true" else "&#9744;"
            attrs_dict["frana_ar"] = "&#9745;" if attrs_dict["frana_ar"] == "true" else "&#9744;"
            attrs_dict["frana_mon"] = "&#9745;" if attrs_dict["frana_mon"] == "true" else "&#9744;"
            attrs_dict["frana_val"] = "&#9745;" if attrs_dict["frana_val"] == "true" else "&#9744;"
            attrs_dict["pai"] = self.pai_dict[attrs_dict["pai"]]
            attrs_dict["alluvio"] = "&#9745;" if attrs_dict["alluvio"] == "true" else "&#9744;"
            attrs_dict["uso_att"] = self.uso_att_dict[attrs_dict["uso_att"]]
            attrs_dict["uso_a"] = "&#9745;" if attrs_dict["uso_a"] == "true" else "&#9744;"
            attrs_dict["uso_a_1"] = attrs_dict["uso_a_1"] if attrs_dict["uso_a_1"] > 0 else "-"
            attrs_dict["uso_b"] = "&#9745;" if attrs_dict["uso_b"] == "true" else "&#9744;"
            attrs_dict["uso_b_1"] = attrs_dict["uso_b_1"] if attrs_dict["uso_b_1"] > 0 else "-"
            attrs_dict["uso_c"] = "&#9745;" if attrs_dict["uso_c"] == "true" else "&#9744;"
            attrs_dict["uso_c_1"] = attrs_dict["uso_c_1"] if attrs_dict["uso_c_1"] > 0 else "-"
            attrs_dict["uso_d"] = "&#9745;" if attrs_dict["uso_d"] == "true" else "&#9744;"
            attrs_dict["uso_d_1"] = attrs_dict["uso_d_1"] if attrs_dict["uso_d_1"] > 0 else "-"
            attrs_dict["uso_e"] = "&#9745;" if attrs_dict["uso_e"] == "true" else "&#9744;"
            attrs_dict["uso_e_1"] = attrs_dict["uso_e_1"] if attrs_dict["uso_e_1"] > 0 else "-"
            attrs_dict["uso_f"] = "&#9745;" if attrs_dict["uso_f"] == "true" else "&#9744;"
            attrs_dict["uso_f_1"] = attrs_dict["uso_f_1"] if attrs_dict["uso_f_1"] > 0 else "-"
            attrs_dict["uso_g"] = "&#9745;" if attrs_dict["uso_g"] == "true" else "&#9744;"
            attrs_dict["uso_g_1"] = attrs_dict["uso_g_1"] if attrs_dict["uso_g_1"] > 0 else "-"
            attrs_dict["epoca_1"] = "&#9745;" if attrs_dict["epoca_1"] == "true" else "&#9744;"
            attrs_dict["epoca_2"] = "&#9745;" if attrs_dict["epoca_2"] == "true" else "&#9744;"
            attrs_dict["epoca_3"] = "&#9745;" if attrs_dict["epoca_3"] == "true" else "&#9744;"
            attrs_dict["epoca_4"] = "&#9745;" if attrs_dict["epoca_4"] == "true" else "&#9744;"
            attrs_dict["epoca_5"] = "&#9745;" if attrs_dict["epoca_5"] == "true" else "&#9744;"
            attrs_dict["epoca_6"] = "&#9745;" if attrs_dict["epoca_6"] == "true" else "&#9744;"
            attrs_dict["epoca_7"] = "&#9745;" if attrs_dict["epoca_7"] == "true" else "&#9744;"
            attrs_dict["epoca_8"] = "&#9745;" if attrs_dict["epoca_8"] == "true" else "&#9744;"
            attrs_dict["utilizz"] = self.utilizz_dict[attrs_dict["utilizz"]]

            html = self.unita_strutt_tmpl.substitute(attrs_dict)

        if html is not None:
            doc = QTextDocument()
            # weird & broken html subset supported by QTextDocument:
            # https://doc.qt.io/qt-5/richtext-html-subset.html
            doc.setHtml(html)
            doc.print(self.printer)
