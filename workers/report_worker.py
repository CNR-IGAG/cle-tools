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

        # with open(os.join("report_templates", "infrastrutture_tmpl.html"), "r") as infrastrutture_tmpl:
        #     self.infrastrutture_tmpl = infrastrutture_tmpl.read()

        # with open(os.join("report_templates", "infrastrutture_tmpl.html"), "r") as infrastrutture_tmpl:
        #     self.infrastrutture_tmpl = infrastrutture_tmpl.read()

        # with open(os.join("report_templates", "infrastrutture_tmpl.html"), "r") as infrastrutture_tmpl:
        #     self.infrastrutture_tmpl = infrastrutture_tmpl.read()

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

        if layer_name.startswith("Infrastrutture"):
            pdf_name = f"{feature['ID_AC']}.pdf"
            pdf_path = os.path.join(self.out_dir, pdf_name)
            self.printer.setOutputFileName(pdf_path)

            attrs_dict = dict(zip(feature.fields().names(), feature.attributes()))
            # substitute values from lookup tables
            attrs_dict['tipo_infra'] = self.tipo_infra_dict[attrs_dict['tipo_infra']]
            attrs_dict['strade_a'] = "&#9745;" if attrs_dict['strade_a'] == "true" else "&#9744;"
            attrs_dict['strade_b'] = "&#9745;" if attrs_dict['strade_b'] == "true" else "&#9744;"
            attrs_dict['strade_c'] = "&#9745;" if attrs_dict['strade_c'] == "true" else "&#9744;"
            attrs_dict['strade_d'] = "&#9745;" if attrs_dict['strade_d'] == "true" else "&#9744;"
            attrs_dict['strade_e'] = "&#9745;" if attrs_dict['strade_e'] == "true" else "&#9744;"
            attrs_dict['strade_f'] = "&#9745;" if attrs_dict['strade_f'] == "true" else "&#9744;"
            attrs_dict['pav_per'] = self.pav_per_dict[attrs_dict['pav_per']]

            # weird & broken html subset supported by QTextDocument:
            # https://doc.qt.io/qt-5/richtext-html-subset.html
            html = self.infrastrutture_tmpl.substitute(attrs_dict)

            doc = QTextDocument()
            # self.set_message.emit(self.css)
            # doc.setDefaultStyleSheet(self.css)
            doc.setHtml(html)
            doc.print(self.printer)

        # time.sleep(1)
