# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:		tb_aggiorna_progetto.py
# Author:	  Tarquini E.
# Created:	 24-09-2018
# -------------------------------------------------------------------------------

import datetime
import os
import shutil
import zipfile

from qgis.core import Qgis, QgsMessageLog, QgsProject
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QDialog, QMessageBox
from qgis.utils import iface

from .utils import save_map_image

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "tb_aggiorna_progetto.ui")
)


class aggiorna_progetto(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)
        self.setupUi(self)
        self.plugin_dir = os.path.dirname(__file__)

    def aggiorna(self, proj_path, dir_output, nome, proj_vers, new_proj_vers):
        self.show()
        result = self.exec_()
        if result:
            try:
                pacchetto = os.path.join(self.plugin_dir, "data", "progetto_CLE.zip")

                if proj_vers < new_proj_vers:

                    name_output = (
                        nome
                        + "_backup_v"
                        + str(proj_vers)
                        + "_"
                        + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
                    )
                    shutil.copytree(proj_path, os.path.join(dir_output, name_output))

                    zip_ref = zipfile.ZipFile(pacchetto, "r")
                    zip_ref.extractall(proj_path)
                    zip_ref.close()

                    shutil.rmtree(os.path.join(proj_path, "progetto", "maschere"))
                    shutil.copytree(
                        os.path.join(proj_path, "progetto_CLE", "progetto", "maschere"),
                        os.path.join(proj_path, "progetto", "maschere"),
                    )
                    shutil.rmtree(os.path.join(proj_path, "progetto", "script"))
                    shutil.copytree(
                        os.path.join(proj_path, "progetto_CLE", "progetto", "script"),
                        os.path.join(proj_path, "progetto", "script"),
                    )
                    os.remove(os.path.join(proj_path, "progetto", "version.txt"))
                    shutil.copyfile(
                        os.path.join(os.path.dirname(__file__), "version.txt"),
                        os.path.join(proj_path, "progetto", "version.txt"),
                    )
                    os.remove(os.path.join(proj_path, "progetto_CLE.qgs"))
                    shutil.copyfile(
                        os.path.join(proj_path, "progetto_CLE", "progetto_CLE.qgs"),
                        os.path.join(proj_path, "progetto_CLE.qgs"),
                    )

                    self.load_new_qgs_file(proj_path)

                    shutil.rmtree(os.path.join(proj_path, "progetto_CLE"))

                    QMessageBox.information(
                        None,
                        self.tr("INFORMATION!"),
                        self.tr(
                            "The project structure has been updated!\nThe backup copy has been saved in the following directory: "
                        )
                        + name_output,
                    )

                    # canvas_extent = iface.mapCanvas().extent()

                    # subset_strings = {}
                    # for vl in QgsProject.instance().mapLayers().values():
                    #     subset_strings[vl.name()] = vl.subsetString()

                    # QgsProject.instance().read(QgsProject.instance().fileName())

                    # for vl in QgsProject.instance().mapLayers().values():
                    #     if subset_strings.get(vl.name(), '') != '':
                    #         vl.setSubsetString(subset_strings.get(vl.name()))

                    # iface.mapCanvas().setExtent(canvas_extent)

            except Exception as z:
                QMessageBox.critical(None, "ERROR!", 'Error:\n"' + str(z) + '"')

    def load_new_qgs_file(self, proj_path):

        QgsMessageLog.logMessage("Loading new project", "CLETools", level=Qgis.Info)

        project = QgsProject.instance()
        project.read(os.path.join(proj_path, "progetto_MS.qgs"))
        comune_layer = QgsProject.instance().mapLayersByName("Comune del progetto")[0]

        features = comune_layer.getFeatures()
        try:
            for feat in features:
                attrs = feat.attributes()
                codice_regio = attrs[1]
                nome = attrs[4]
                regione = attrs[7]
        except IndexError:
            regione = ""

        sourceLYR = QgsProject.instance().mapLayersByName("Limiti comunali")[0]
        sourceLYR.setSubsetString("cod_regio='" + codice_regio + "'")
        canvas = iface.mapCanvas()
        comune_extent = comune_layer.extent()

        layout_manager = QgsProject.instance().layoutManager()
        layouts = layout_manager.printLayouts()

        # replace region logo
        logo_regio_in = os.path.join(
            self.plugin_dir, "img", "logo_regio", codice_regio + ".png"
        ).replace("\\", "/")
        logo_regio_out = os.path.join(
            proj_path, "progetto", "loghi", "logo_regio.png"
        ).replace("\\", "/")
        shutil.copyfile(logo_regio_in, logo_regio_out)

        # replace region map
        layer_tree_root = QgsProject.instance().layerTreeRoot()
        project_layers = layer_tree_root.layerOrder()
        for layer in project_layers:
            layer_tree_root.findLayer(layer.id()).setItemVisibilityChecked(False)
        layer_limiti_comunali = QgsProject.instance().mapLayersByName(
            "Limiti comunali"
        )[0]
        layer_tree_root.findLayer(layer_limiti_comunali.id()).setItemVisibilityChecked(
            True
        )
        layer_tree_root.findLayer(comune_layer.id()).setItemVisibilityChecked(True)
        imageFilename = os.path.join(proj_path, "progetto", "loghi", "mappa_reg.png")
        save_map_image(imageFilename, layer_limiti_comunali, canvas)

        canvas.setExtent(comune_extent)

        for layout in layouts:
            map_item = layout.itemById("mappa_0")
            map_item.zoomToExtent(canvas.extent())
            map_item_2 = layout.itemById("regio_title")
            map_item_2.setText("Regione " + regione)
            map_item_3 = layout.itemById("com_title")
            map_item_3.setText("Comune di " + nome)
            map_item_4 = layout.itemById("logo")
            map_item_4.refreshPicture()
            map_item_5 = layout.itemById("mappa_1")
            map_item_5.refreshPicture()

    def tr(self, message):
        return QCoreApplication.translate("aggiorna_progetto", message)
