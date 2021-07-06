# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:		CLETools.py
# Author:	  Tarquini E.
# Created:	 15-01-2019
# -------------------------------------------------------------------------------
import os
import shutil

from qgis.core import (
    Qgis,
    QgsMessageLog,
    QgsProject,
    QgsSettings,
    QgsSnappingConfig,
    QgsTolerance,
)
from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog, qApp

from .tb_aggiorna_progetto import aggiorna_progetto
from .tb_esporta_shp import esporta_shp
from .tb_info import info
from .tb_nuovo_progetto import nuovo_progetto
from .tb_generate_reports import ReportGen

# from .tb_wait import wait


class CLETools(object):
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        try:
            locale = QSettings().value("locale/userLocale", "en", type=str)[0:2]
        except Exception:
            locale = "en"
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "CLETools_{}.qm".format(locale)
        )
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # self.dlg_wait = wait()
        self.dlg_project_update = aggiorna_progetto()
        self.dlg_new_project = nuovo_progetto()
        self.dlg_info = info()
        self.dlg_export_shp = esporta_shp()
        
        # report generation tool
        self.dlg_generate_reports = ReportGen()
        self.dlg_generate_reports.pushButton_out.clicked.connect(self.select_output_fld_report)

        self.actions = []
        self.menu = self.tr("&CLE Tools")
        self.toolbar = self.iface.addToolBar("CLETools")
        self.toolbar.setObjectName("CLETools")

        self.dlg_new_project.dir_output.clear()
        self.dlg_new_project.pushButton_out.clicked.connect(self.select_output_fld_2)

        self.dlg_export_shp.dir_output.clear()
        self.dlg_export_shp.pushButton_out.clicked.connect(self.select_output_fld_5)

        QgsSettings().setValue("qgis/enableMacros", 3)

        self.iface.projectRead.connect(self.check_project)

    def tr(self, message):
        return QCoreApplication.translate("CLETools", message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToDatabaseMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self):
        icons_path = os.path.join(self.plugin_dir, "img")

        self.add_action(
            os.path.join(icons_path, "ico_nuovo_progetto.png"),
            text=self.tr("New project"),
            callback=self.new_project,
            parent=self.iface.mainWindow(),
        )

        self.toolbar.addSeparator()

        self.add_action(
            os.path.join(icons_path, "ico_esporta.png"),
            text=self.tr("Export geodatabase to project folder"),
            callback=self.export_database,
            parent=self.iface.mainWindow(),
        )

        self.toolbar.addSeparator()

        self.add_action(
            os.path.join(icons_path, "ico_edita.png"),
            text=self.tr("Add feature or record"),
            callback=self.add_feature_or_record,
            parent=self.iface.mainWindow(),
        )

        self.add_action(
            os.path.join(icons_path, "ico_salva_edita.png"),
            text=self.tr("Save"),
            callback=self.save,
            parent=self.iface.mainWindow(),
        )

        self.toolbar.addSeparator()

        self.add_action(
            os.path.join(icons_path, "ico_pdf.png"),
            text=self.tr("Generate reports"),
            callback=self.generate_reports,
            parent=self.iface.mainWindow(),
        )

        self.add_action(
            os.path.join(icons_path, "ico_info.png"),
            text=self.tr("Help"),
            callback=self.help,
            parent=self.iface.mainWindow(),
        )

    def unload(self):
        for action in self.actions:
            self.iface.removePluginDatabaseMenu(self.tr("&CLE Tools"), action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def select_output_fld_2(self):
        out_dir = QFileDialog.getExistingDirectory(
            self.dlg_new_project, "", "", QFileDialog.ShowDirsOnly
        )
        self.dlg_new_project.dir_output.setText(out_dir)

    def select_input_fld_5(self):
        in_dir = QFileDialog.getExistingDirectory(
            self.dlg_export_shp, "", "", QFileDialog.ShowDirsOnly
        )
        self.dlg_export_shp.dir_input.setText(in_dir)

    def select_output_fld_5(self):
        out_dir = QFileDialog.getExistingDirectory(
            self.dlg_export_shp, "", "", QFileDialog.ShowDirsOnly
        )
        self.dlg_export_shp.dir_output.setText(out_dir)

    def select_output_fld_report(self):
        out_dir = QFileDialog.getExistingDirectory(
            self.dlg_generate_reports, "", "", QFileDialog.ShowDirsOnly
        )
        self.dlg_generate_reports.dir_output.setText(out_dir)

    def check_project(self):
        percorso = QgsProject.instance().homePath()
        dir_output = "/".join(percorso.split("/")[:-1])
        nome = percorso.split("/")[-1]

        # detect CLETools project
        if os.path.exists(os.path.join(percorso, "progetto")) and os.path.exists(
            os.path.join(percorso, "progetto", "version.txt")
        ):
            QgsMessageLog.logMessage("CLETools project detected", "CLETools", Qgis.Info)
            QgsMessageLog.logMessage("Checking svg symbols...", "CLETools", Qgis.Info)

            dir_svg_input = os.path.join(self.plugin_dir, "img", "svg")
            dir_svg_output = self.plugin_dir.split("python")[0] + "svg"

            if not os.path.exists(dir_svg_output):
                QgsMessageLog.logMessage(
                    f"Copying svg symbols in {dir_svg_output}", "CLETools", Qgis.Info
                )
                shutil.copytree(dir_svg_input, dir_svg_output)
            else:
                QgsMessageLog.logMessage(
                    f"Updating svg symbols in {dir_svg_output}", "CLETools", Qgis.Info
                )
                src_files = os.listdir(dir_svg_input)
                for file_name in src_files:
                    full_file_name = os.path.join(dir_svg_input, file_name)
                    if os.path.isfile(full_file_name):
                        shutil.copy(full_file_name, dir_svg_output)

            vers_data = os.path.join(
                os.path.dirname(QgsProject.instance().fileName()),
                "progetto",
                "version.txt",
            )
            try:
                with open(vers_data, "r") as f:
                    proj_vers = float(f.read())
                    with open(
                        os.path.join(os.path.dirname(__file__), "version.txt")
                    ) as nf:
                        new_proj_vers = float(nf.read())
                        if proj_vers < new_proj_vers:
                            QgsMessageLog.logMessage(
                                "Project needs updating!", "CLETools", Qgis.Info
                            )
                            qApp.processEvents()
                            self.dlg_project_update.aggiorna(
                                percorso, dir_output, nome, proj_vers, new_proj_vers
                            )

            except Exception as ex:
                QgsMessageLog.logMessage("Error: %s" % ex, "CLE Tools")

    def new_project(self):
        self.dlg_new_project.nuovo()

    def help(self):
        self.dlg_info.help()

    def export_database(self):
        self.dlg_export_shp.esporta_prog()

    def generate_reports(self):
        self.dlg_generate_reports.generate_reports()

    def add_feature_or_record(self):
        proj = QgsProject.instance()

        snapping_config = proj.instance().snappingConfig()
        snapping_config.clearIndividualLayerSettings()

        snapping_config.setTolerance(20.0)
        snapping_config.setMode(QgsSnappingConfig.AllLayers)

        DIZIO_LAYER = {
            "Aree di emergenza": [
                "Aggregati strutturali",
                "Edifici strategici",
                "Unita' strutturali",
            ],
            "Edifici strategici": ["Aree di emergenza", "Unita' strutturali"],
            "Aggregati strutturali": ["Aree di emergenza"],
            "Unita' strutturali": ["Aree di emergenza", "Edifici strategici"],
        }
        POLY_LYR = [
            "Aree di emergenza",
            "Aggregati strutturali",
            "Edifici strategici",
            "Unita' strutturali",
        ]

        layer = self.iface.activeLayer()
        if layer is not None:
            if layer.name() in POLY_LYR:

                # self.dlg_wait.show()
                for fc in proj.mapLayers().values():
                    if fc.name() in POLY_LYR:
                        layer_settings = QgsSnappingConfig.IndividualLayerSettings(
                            True,
                            QgsSnappingConfig.VertexFlag,
                            20,
                            QgsTolerance.ProjectUnits,
                        )

                        snapping_config.setIndividualLayerSettings(fc, layer_settings)
                        snapping_config.setIntersectionSnapping(False)

                for chiave, valore in DIZIO_LAYER.items():
                    if layer.name() == chiave:
                        for layer_name in valore:

                            other_layer = QgsProject.instance().mapLayersByName(
                                layer_name
                            )[0]
                            layer_settings = QgsSnappingConfig.IndividualLayerSettings(
                                True,
                                QgsSnappingConfig.VertexFlag,
                                20,
                                QgsTolerance.ProjectUnits,
                            )
                            snapping_config.setIndividualLayerSettings(
                                layer, layer_settings
                            )
                            snapping_config.setIndividualLayerSettings(
                                other_layer, layer_settings
                            )

                        snapping_config.setIntersectionSnapping(True)

                layer.startEditing()
                self.iface.actionAddFeature().trigger()
                # self.dlg_wait.hide()

            else:
                layer.startEditing()
                self.iface.actionAddFeature().trigger()

    def save(self):

        proj = QgsProject.instance()
        POLYGON_LYR = [
            "Aree di emergenza",
            "Aggregati strutturali",
            "Edifici strategici",
            "Unita' strutturali",
        ]

        snapping_config = proj.snappingConfig()
        snapping_config.clearIndividualLayerSettings()

        snapping_config.setTolerance(20.0)
        snapping_config.setMode(QgsSnappingConfig.AllLayers)

        layer = self.iface.activeLayer()
        if layer is not None:
            if layer.name() in POLYGON_LYR:

                # self.dlg_wait.show()
                layers = proj.mapLayers().values()

                for fc in layers:
                    if fc.name() in POLYGON_LYR:
                        layer_settings = QgsSnappingConfig.IndividualLayerSettings(
                            True,
                            QgsSnappingConfig.VertexFlag,
                            20,
                            QgsTolerance.ProjectUnits,
                        )
                        snapping_config.setIndividualLayerSettings(fc, layer_settings)

                layer.commitChanges()
                # self.dlg_wait.hide()

            else:
                layer.commitChanges()
