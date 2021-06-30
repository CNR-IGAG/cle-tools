import os
import time

from qgis.core import (
    Qgis,
    QgsMessageLog,
    QgsProject,
    QgsSettings,
    QgsSnappingConfig,
    QgsTolerance,
)
from qgis.gui import *
from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator
from qgis.PyQt.QtGui import QTextDocument
from qgis.PyQt.QtWidgets import QAction, QFileDialog, qApp
from qgis.PyQt.QtPrintSupport import QPrinter
from string import Template

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
        # self.printer.setPageMargins(10, 10, 10, 10, QPrinter.Millimeter)
        self.printer.setFullPage(True)
        self.printer.setOutputFormat(QPrinter.PdfFormat)

        # load templates
        with open(os.path.join(os.path.dirname(__file__), "report_templates", "infrastrutture_tmpl.html"), "r") as f:
            self.infrastrutture_tmpl = Template(f.read())

        with open(os.path.join(os.path.dirname(__file__), "report_templates", "aree_emerg_tmpl.html"), "r") as f:
            self.aree_emerg_tmpl = Template(f.read())

        with open(os.path.join(os.path.dirname(__file__), "report_templates", "aggregati_tmpl.html"), "r") as f:
            self.aggregati_tmpl = Template(f.read())

        # load lookup tables
        self.tipo_infra_dict = {}
        vw_tipo_infra = QgsProject.instance().mapLayersByName("vw_tipo_infra")[0]
        for f in vw_tipo_infra.getFeatures():
            self.tipo_infra_dict[f['cod']] = f['descrizione']

        self.pav_per_dict = {}
        vw_pav_per = QgsProject.instance().mapLayersByName("vw_pav_per")[0]
        for f in vw_pav_per.getFeatures():
            self.pav_per_dict[f['cod']] = f['descrizione']

        self.ost_disc_dict = {}
        vw_ost_disc = QgsProject.instance().mapLayersByName("vw_ost_disc")[0]
        for f in vw_ost_disc.getFeatures():
            self.ost_disc_dict[f['cod']] = f['descrizione']

        self.morf_dict = {}
        vw_morf = QgsProject.instance().mapLayersByName("vw_morf")[0]
        for f in vw_morf.getFeatures():
            self.morf_dict[f['cod']] = f['descrizione']

        self.zona_ms_dict = {}
        vw_zona_ms = QgsProject.instance().mapLayersByName("vw_zona_ms")[0]
        for f in vw_zona_ms.getFeatures():
            self.zona_ms_dict[f['cod']] = f['descrizione']

        self.falda_dict = {}
        vw_falda = QgsProject.instance().mapLayersByName("vw_falda")[0]
        for f in vw_falda.getFeatures():
            self.falda_dict[f['cod']] = f['descrizione']

        self.acq_sup_dict = {}
        vw_acq_sup = QgsProject.instance().mapLayersByName("vw_acq_sup")[0]
        for f in vw_acq_sup.getFeatures():
            self.acq_sup_dict[f['cod']] = f['descrizione']

        self.pai_dict = {}
        vw_pai = QgsProject.instance().mapLayersByName("vw_pai")[0]
        for f in vw_pai.getFeatures():
            self.pai_dict[f['cod']] = f['descrizione']

        self.tipo_area_dict = {}
        vw_tipo_area = QgsProject.instance().mapLayersByName("vw_tipo_area")[0]
        for f in vw_tipo_area.getFeatures():
            self.tipo_area_dict[f['cod']] = f['descrizione']

        self.piano_dict = {}
        vw_piano = QgsProject.instance().mapLayersByName("vw_piano")[0]
        for f in vw_piano.getFeatures():
            self.piano_dict[f['cod']] = f['descrizione']

        self.infra_acq_dict = {}
        vw_infra_acq = QgsProject.instance().mapLayersByName("vw_infra_acq")[0]
        for f in vw_infra_acq.getFeatures():
            self.infra_acq_dict[f['cod']] = f['descrizione']
        
        self.infra_ele_dict = {}
        vw_infra_ele = QgsProject.instance().mapLayersByName("vw_infra_ele")[0]
        for f in vw_infra_ele.getFeatures():
            self.infra_ele_dict[f['cod']] = f['descrizione']

        self.infra_fog_dict = {}
        vw_infra_fog = QgsProject.instance().mapLayersByName("vw_infra_fog")[0]
        for f in vw_infra_fog.getFeatures():
            self.infra_fog_dict[f['cod']] = f['descrizione']

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
            pdf_path = os.path.join(self.out_dir, pdf_name)
            self.printer.setOutputFileName(pdf_path)

            # substitute codes with corresponding values from lookup tables
            attrs_dict['tipo_infra'] = self.tipo_infra_dict[attrs_dict['tipo_infra']]
            attrs_dict['strade_a'] = "&#9745;" if attrs_dict['strade_a'] == "true" else "&#9744;"
            attrs_dict['strade_b'] = "&#9745;" if attrs_dict['strade_b'] == "true" else "&#9744;"
            attrs_dict['strade_c'] = "&#9745;" if attrs_dict['strade_c'] == "true" else "&#9744;"
            attrs_dict['strade_d'] = "&#9745;" if attrs_dict['strade_d'] == "true" else "&#9744;"
            attrs_dict['strade_e'] = "&#9745;" if attrs_dict['strade_e'] == "true" else "&#9744;"
            attrs_dict['strade_f'] = "&#9745;" if attrs_dict['strade_f'] == "true" else "&#9744;"
            attrs_dict['pav_per'] = self.pav_per_dict[attrs_dict['pav_per']]
            attrs_dict['ost_disc'] = self.ost_disc_dict[attrs_dict['ost_disc']]
            attrs_dict['morf'] = self.morf_dict[attrs_dict['morf']]
            attrs_dict['ubic_sotto'] = "&#9745;" if attrs_dict['ubic_sotto'] == "true" else "&#9744;"
            attrs_dict['ubic_sopra'] = "&#9745;" if attrs_dict['ubic_sopra'] == "true" else "&#9744;"
            attrs_dict['zona_ms'] = self.zona_ms_dict[attrs_dict['zona_ms']]
            attrs_dict['inst_fran'] = "&#9745;" if attrs_dict['inst_fran'] == "true" else "&#9744;"
            attrs_dict['inst_liq'] = "&#9745;" if attrs_dict['inst_liq'] == "true" else "&#9744;"
            attrs_dict['inst_fag'] = "&#9745;" if attrs_dict['inst_fag'] == "true" else "&#9744;"
            attrs_dict['inst_ced'] = "&#9745;" if attrs_dict['inst_ced'] == "true" else "&#9744;"
            attrs_dict['inst_cav'] = "&#9745;" if attrs_dict['inst_cav'] == "true" else "&#9744;"
            attrs_dict['frana_AC'] = "&#9745;" if attrs_dict['frana_AC'] == "true" else "&#9744;"
            attrs_dict['frana_mon'] = "&#9745;" if attrs_dict['frana_mon'] == "true" else "&#9744;"
            attrs_dict['frana_val'] = "&#9745;" if attrs_dict['frana_val'] == "true" else "&#9744;"
            attrs_dict['falda'] = self.falda_dict[attrs_dict['falda']]
            attrs_dict['acq_sup'] = self.acq_sup_dict[attrs_dict['acq_sup']]
            attrs_dict['pai'] = self.pai_dict[attrs_dict['pai']]
            attrs_dict['alluvio'] = "&#9745;" if attrs_dict['alluvio'] == "true" else "&#9744;"

            # weird & broken html subset supported by QTextDocument:
            # https://doc.qt.io/qt-5/richtext-html-subset.html
            html = self.infrastrutture_tmpl.substitute(attrs_dict)

        elif layer_name.startswith("Aree"):
            pdf_name = f"{feature['ID_AE']}.pdf"
            pdf_path = os.path.join(self.out_dir, pdf_name)
            self.printer.setOutputFileName(pdf_path)

            # substitute codes with corresponding values from lookup tables
            attrs_dict['tipo_area'] = self.tipo_area_dict[attrs_dict['tipo_area']]
            attrs_dict['piano'] = self.piano_dict[attrs_dict['piano']]
            attrs_dict['pav_per'] = self.pav_per_dict[attrs_dict['pav_per']]
            attrs_dict['infra_acq'] = self.infra_acq_dict[attrs_dict['infra_acq']]
            attrs_dict['infra_ele'] = self.infra_ele_dict[attrs_dict['infra_ele']]
            attrs_dict['infra_fog'] = self.infra_fog_dict[attrs_dict['infra_fog']]
            attrs_dict['morf'] = self.morf_dict[attrs_dict['morf']]
            attrs_dict['ubic_sotto'] = "&#9745;" if attrs_dict['ubic_sotto'] == "true" else "&#9744;"
            attrs_dict['ubic_sopra'] = "&#9745;" if attrs_dict['ubic_sopra'] == "true" else "&#9744;"
            attrs_dict['zona_ms'] = self.zona_ms_dict[attrs_dict['zona_ms']]
            attrs_dict['inst_fran'] = "&#9745;" if attrs_dict['inst_fran'] == "true" else "&#9744;"
            attrs_dict['inst_liq'] = "&#9745;" if attrs_dict['inst_liq'] == "true" else "&#9744;"
            attrs_dict['inst_fag'] = "&#9745;" if attrs_dict['inst_fag'] == "true" else "&#9744;"
            attrs_dict['inst_ced'] = "&#9745;" if attrs_dict['inst_ced'] == "true" else "&#9744;"
            attrs_dict['inst_cav'] = "&#9745;" if attrs_dict['inst_cav'] == "true" else "&#9744;"
            attrs_dict['frana_AE'] = "&#9745;" if attrs_dict['frana_AE'] == "true" else "&#9744;"
            attrs_dict['frana_mon'] = "&#9745;" if attrs_dict['frana_mon'] == "true" else "&#9744;"
            attrs_dict['frana_val'] = "&#9745;" if attrs_dict['frana_val'] == "true" else "&#9744;"
            attrs_dict['falda'] = self.falda_dict[attrs_dict['falda']]
            attrs_dict['acq_sup'] = self.acq_sup_dict[attrs_dict['acq_sup']]
            attrs_dict['pai'] = self.pai_dict[attrs_dict['pai']]
            attrs_dict['alluvio'] = "&#9745;" if attrs_dict['alluvio'] == "true" else "&#9744;"

            html = self.aree_emerg_tmpl.substitute(attrs_dict)

        elif layer_name.startswith("Aggregati"):
            pdf_name = f"{feature['ID_AS']}.pdf"
            pdf_path = os.path.join(self.out_dir, pdf_name)
            self.printer.setOutputFileName(pdf_path)

            # substitute codes with corresponding values from lookup tables
            attrs_dict['conn_volte'] = "&#9745;" if attrs_dict['conn_volte'] == "true" else "&#9744;"
            attrs_dict['conn_rifus'] = "&#9745;" if attrs_dict['conn_rifus'] == "true" else "&#9744;"
            attrs_dict['regol_1'] = "&#9745;" if attrs_dict['regol_1'] == "true" else "&#9744;"
            attrs_dict['regol_2'] = "&#9745;" if attrs_dict['regol_2'] == "true" else "&#9744;"
            attrs_dict['regol_3'] = "&#9745;" if attrs_dict['regol_3'] == "true" else "&#9744;"
            attrs_dict['regol_4'] = "&#9745;" if attrs_dict['regol_4'] == "true" else "&#9744;"
            attrs_dict['regol_5'] = "&#9745;" if attrs_dict['regol_5'] == "true" else "&#9744;"
            attrs_dict['vuln_1'] = "&#9745;" if attrs_dict['vuln_1'] == "true" else "&#9744;"
            attrs_dict['vuln_2'] = "&#9745;" if attrs_dict['vuln_2'] == "true" else "&#9744;"
            attrs_dict['vuln_3'] = "&#9745;" if attrs_dict['vuln_3'] == "true" else "&#9744;"
            attrs_dict['vuln_4'] = "&#9745;" if attrs_dict['vuln_4'] == "true" else "&#9744;"
            attrs_dict['vuln_5'] = "&#9745;" if attrs_dict['vuln_5'] == "true" else "&#9744;"
            attrs_dict['vuln_6'] = "&#9745;" if attrs_dict['vuln_6'] == "true" else "&#9744;"
            attrs_dict['rinfor_1'] = "&#9745;" if attrs_dict['rinfor_1'] == "true" else "&#9744;"
            attrs_dict['rinfor_2'] = "&#9745;" if attrs_dict['rinfor_2'] == "true" else "&#9744;"
            attrs_dict['morf'] = self.morf_dict[attrs_dict['morf']]
            attrs_dict['ubic_sotto'] = "&#9745;" if attrs_dict['ubic_sotto'] == "true" else "&#9744;"
            attrs_dict['ubic_sopra'] = "&#9745;" if attrs_dict['ubic_sopra'] == "true" else "&#9744;"
            attrs_dict['zona_ms'] = self.zona_ms_dict[attrs_dict['zona_ms']]
            attrs_dict['inst_fran'] = "&#9745;" if attrs_dict['inst_fran'] == "true" else "&#9744;"
            attrs_dict['inst_liq'] = "&#9745;" if attrs_dict['inst_liq'] == "true" else "&#9744;"
            attrs_dict['inst_fag'] = "&#9745;" if attrs_dict['inst_fag'] == "true" else "&#9744;"
            attrs_dict['inst_ced'] = "&#9745;" if attrs_dict['inst_ced'] == "true" else "&#9744;"
            attrs_dict['inst_cav'] = "&#9745;" if attrs_dict['inst_cav'] == "true" else "&#9744;"
            attrs_dict['frana_AS'] = "&#9745;" if attrs_dict['frana_AS'] == "true" else "&#9744;"
            attrs_dict['frana_mon'] = "&#9745;" if attrs_dict['frana_mon'] == "true" else "&#9744;"
            attrs_dict['frana_val'] = "&#9745;" if attrs_dict['frana_val'] == "true" else "&#9744;"
            attrs_dict['pai'] = self.pai_dict[attrs_dict['pai']]
            attrs_dict['alluvio'] = "&#9745;" if attrs_dict['alluvio'] == "true" else "&#9744;"

            html = self.aggregati_tmpl.substitute(attrs_dict)

        if html is not None:
            doc = QTextDocument()
            # self.set_message.emit(self.css)
            # doc.setDefaultStyleSheet(self.css)
            doc.setHtml(html)
            doc.print(self.printer)

        # time.sleep(1)
