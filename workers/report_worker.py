import os
import shutil
import sqlite3
import sys
import webbrowser
import zipfile
import time

from ..constants import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt import uic
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.utils import *

from qgis.PyQt.QtPrintSupport import QPrinter

from .abstract_worker import AbstractWorker, UserAbortedNotification


class ReportWorker(AbstractWorker):
    """Worker class handling report generation"""

    def __init__(self, out_dir):
        super().__init__()
        self.out_dir = out_dir
        self.current_step = 1

    def work(self):
        # list layers
        self.set_message.emit("Getting feature list...")

        # list features for all layers
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
            printer = QPrinter()
            printer.setPageSize(QPrinter.A4)
            # printer.setPageMargins(10, 10, 10, 10, QPrinter.Millimeter)
            printer.setFullPage(True)
            printer.setOutputFormat(QPrinter.PdfFormat)
            pdf_name = f"{feature['ID_AC']}.pdf"
            pdf_path = os.path.join(self.out_dir, pdf_name)
            printer.setOutputFileName(pdf_path)

            # weird & broken html subset supported by QTextDocument:
            # https://doc.qt.io/qt-5/richtext-html-subset.html
            html = f"""
                <!DOCTYPE html>
                <html>
                    <head>
                        <style>
                            body {{
                                font-size: 11px;
                                color: #222222;
                            }}
                        </style>
                    </head>
                    <body>
                        <h3 align="center">Analisi della condizione limite per l'emergenza dell'insediamento urbano</h3>
                        <h2 align="center">Infrastrutture di accessibilità/connessione (AC)</h2>
                        
                        <hr>

                        <h3 align="center">Identificativi</h3>

                        <table width="100%">
                            <tr>
                                <td>ID_AC:</td>
                                <td align="right"><strong>{feature['ID_AC']}</strong></td>
                            </tr>
                            <tr>
                                <td>Data Compilazione:</td>
                                <td align="right"><strong>{feature['data_ac']}</strong></td>
                            </tr>
                        </table>

                        <div>
                            <table width="100%">
                                <caption><strong>Codice ISTAT</strong></caption>
                                <tr style="background-color: #f0f0f0;">
                                    <td><em>Regione</em></td>
                                    <td>{feature['regione']}</td>
                                    <td>{feature['cod_reg']}</td>
                                </tr>
                                <tr style="background-color: #f0f0f0;">
                                    <td><em>Provincia</em></td>
                                    <td>{feature['provincia']}</td>
                                    <td>{feature['cod_prov']}</td>
                                </tr>
                                <tr style="background-color: #f0f0f0;">
                                    <td><em>Comune</em></td>
                                    <td>{feature['comune']}</td>
                                    <td>{feature['cod_com']}</td>
                                </tr>
                            </table>
                        </div>
                        
                        <p>Località abitata: {feature['localita']}</p>
                        <p>Tipo infrastruttura: {feature['tipo_infra']}</p>
                        <p>Identificativo infrastrutture di Accessibilità/Connessione: {feature['ID_infra']}</p>

                    </body>
                </html>
            """

            doc = QTextDocument()
            # self.set_message.emit(self.css)
            # doc.setDefaultStyleSheet(self.css)
            doc.setHtml(html)
            doc.print(printer)

        time.sleep(1)
