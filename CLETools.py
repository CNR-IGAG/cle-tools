# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:		CLETools.py
# Author:	  Tarquini E.
# Created:	 15-01-2019
# -------------------------------------------------------------------------------
import os
import sys

from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.utils import *

from . import constants
from .tb_aggiorna_progetto import aggiorna_progetto
#from tb_importa_shp import importa_shp
from .tb_esporta_shp import esporta_shp
#from tb_report_cle import report_cle
from .tb_info import info
from .tb_nuovo_progetto import nuovo_progetto
from .tb_wait import wait


class CLETools(object):

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CLETools_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.dlg_wait = wait()
        self.dlg_project_update = aggiorna_progetto()
        self.dlg_new_project = nuovo_progetto()
        self.dlg_info = info()
        self.dlg_export_shp = esporta_shp()

        self.actions = []
        self.menu = self.tr('&CLE Tools')
        self.toolbar = self.iface.addToolBar('CLETools')
        self.toolbar.setObjectName('CLETools')

        self.dlg_new_project.dir_output.clear()
        self.dlg_new_project.pushButton_out.clicked.connect(
            self.select_output_fld_2)

        self.dlg_export_shp.dir_output.clear()
        self.dlg_export_shp.pushButton_out.clicked.connect(
            self.select_output_fld_5)

        self.iface.projectRead.connect(self.run1)

    def tr(self, message):
        return QCoreApplication.translate('CLETools', message)

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
            parent=None):

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
            self.iface.addPluginToDatabaseMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        icon_path2 = self.plugin_dir + os.sep + \
            "img" + os.sep + 'ico_nuovo_progetto.png'
        icon_path3 = self.plugin_dir + os.sep + "img" + os.sep + 'ico_info.png'
        icon_path5 = self.plugin_dir + os.sep + "img" + os.sep + 'ico_esporta.png'
        icon_path7 = self.plugin_dir + os.sep + "img" + os.sep + 'ico_edita.png'
        icon_path8 = self.plugin_dir + os.sep + "img" + os.sep + 'ico_salva_edita.png'

        self.add_action(
            icon_path2,
            text=self.tr('New project'),
            callback=self.new_project,
            parent=self.iface.mainWindow())

        self.toolbar.addSeparator()

        self.add_action(
            icon_path5,
            text=self.tr('Export geodatabase to project folder'),
            callback=self.export_database,
            parent=self.iface.mainWindow())

        self.toolbar.addSeparator()

        self.add_action(
            icon_path7,
            text=self.tr('Add feature or record'),
            callback=self.add_feature_or_record,
            parent=self.iface.mainWindow())

        self.add_action(
            icon_path8,
            text=self.tr('Save'),
            callback=self.save,
            parent=self.iface.mainWindow())

        self.toolbar.addSeparator()

        self.add_action(
            icon_path3,
            text=self.tr('Help'),
            callback=self.help,
            parent=self.iface.mainWindow())

    def unload(self):
        for action in self.actions:
            self.iface.removePluginDatabaseMenu(
                self.tr('&CLE Tools'),
                action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def select_output_fld_2(self):
        out_dir = QFileDialog.getExistingDirectory(
            self.dlg_new_project, "", "", QFileDialog.ShowDirsOnly)
        self.dlg_new_project.dir_output.setText(out_dir)

    def select_input_fld_5(self):
        in_dir = QFileDialog.getExistingDirectory(
            self.dlg_export_shp, "", "", QFileDialog.ShowDirsOnly)
        self.dlg_export_shp.dir_input.setText(in_dir)

    def select_output_fld_5(self):
        out_dir = QFileDialog.getExistingDirectory(
            self.dlg_export_shp, "", "", QFileDialog.ShowDirsOnly)
        self.dlg_export_shp.dir_output.setText(out_dir)

    def run1(self):
        percorso = QgsProject.instance().homePath()
        dir_output = '/'.join(percorso.split('/')[:-1])
        nome = percorso.split('/')[-1]
        if os.path.exists(percorso + os.sep + "progetto"):
            vers_data = (QgsProject.instance().fileName()).split("progetto")[
                0] + os.sep + "progetto" + os.sep + "version.txt"
            try:
                proj_vers = open(vers_data, 'r').read()
                if proj_vers < '0.3':
                    qApp.processEvents()
                    self.dlg_project_update.aggiorna(
                        percorso, dir_output, nome)

            except:
                pass

    def new_project(self):
        self.dlg_new_project.nuovo()

    def help(self):
        self.dlg_info.help()

    def export_database(self):
        self.dlg_export_shp.esporta_prog()

    def add_feature_or_record(self):
        proj = QgsProject.instance()

        snapping_config = proj.instance().snappingConfig()
        snapping_config.clearIndividualLayerSettings()

        snapping_config.setTolerance(20.0)
        snapping_config.setMode(QgsSnappingConfig.AllLayers)

        DIZIO_LAYER = {"Aree di emergenza": ["Aggregati strutturali", "Edifici strategici", "Unita' strutturali"],
                       "Edifici strategici": ["Aree di emergenza", "Unita' strutturali"],
                       "Aggregati strutturali": ["Aree di emergenza"],
                       "Unita' strutturali": ["Aree di emergenza", "Edifici strategici"]}
        POLY_LYR = ["Aree di emergenza", "Aggregati strutturali",
                    "Edifici strategici", "Unita' strutturali"]

        layer = iface.activeLayer()
        if layer != None:
            if layer.name() in POLY_LYR:

                self.dlg_wait.show()
                for fc in proj.mapLayers().values():
                    if fc.name() in POLY_LYR:
                        layer_settings = QgsSnappingConfig.IndividualLayerSettings(
                            True, QgsSnappingConfig.Vertex, 20, QgsTolerance.ProjectUnits)

                        snapping_config.setIndividualLayerSettings(
                            fc, layer_settings)
                        snapping_config.setIntersectionSnapping(False)

                for chiave, valore in DIZIO_LAYER.items():
                    if layer.name() == chiave:
                        for layer_name in valore:

                            other_layer = QgsProject.instance().mapLayersByName(layer_name)[
                                0]
                            layer_settings = QgsSnappingConfig.IndividualLayerSettings(
                                True, QgsSnappingConfig.Vertex, 20, QgsTolerance.ProjectUnits)
                            snapping_config.setIndividualLayerSettings(
                                layer, layer_settings)
                            snapping_config.setIndividualLayerSettings(
                                other_layer, layer_settings)

                        snapping_config.setIntersectionSnapping(True)

                layer.startEditing()
                iface.actionAddFeature().trigger()
                self.dlg_wait.hide()

            else:
                layer.startEditing()
                iface.actionAddFeature().trigger()

    def save(self):

        proj = QgsProject.instance()
        POLYGON_LYR = ["Aree di emergenza", "Aggregati strutturali",
                       "Edifici strategici", "Unita' strutturali"]

        snapping_config = proj.snappingConfig()
        snapping_config.clearIndividualLayerSettings()

        snapping_config.setTolerance(20.0)
        snapping_config.setMode(QgsSnappingConfig.AllLayers)

        layer = iface.activeLayer()
        if layer != None:
            if layer.name() in POLYGON_LYR:

                self.dlg_wait.show()
                layers = proj.mapLayers().values()

                for fc in layers:
                    if fc.name() in POLYGON_LYR:
                        layer_settings = QgsSnappingConfig.IndividualLayerSettings(
                            True, QgsSnappingConfig.Vertex, 20, QgsTolerance.ProjectUnits)
                        snapping_config.setIndividualLayerSettings(
                            fc, layer_settings)

                layer.commitChanges()
                self.dlg_wait.hide()

            else:
                layer.commitChanges()
