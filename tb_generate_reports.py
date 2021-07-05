import os

from qgis.core import QgsProject
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QDialog, QMessageBox
from qgis.utils import iface

from .setup_workers import setup_workers
from .workers.report_worker import ReportWorker

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "tb_generate_reports.ui")
)


class ReportGen(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        self.iface = iface
        super().__init__(parent)
        self.setupUi(self)
        self.plugin_dir = os.path.dirname(__file__)

    def generate_reports(self):

        # TODO: connect to docs
        self.help_button.setEnabled(False)
        self.dir_output.clear()

        root = QgsProject.instance().layerTreeRoot()
        cle_group = root.findGroup("CLE")
        if cle_group:
            self.alert_text.hide()
        else:
            self.alert_text.show()

        self.button_box.setEnabled(False)
        self.dir_output.textChanged.connect(self.validate_input)

        self.show()
        result = self.exec_()
        if result:
            try:
                # in_dir = QgsProject.instance().readPath("./")
                out_dir = self.dir_output.text()
                if os.path.exists(out_dir):

                    # create export worker
                    worker = ReportWorker(out_dir)

                    # start export worker
                    worker_manager = setup_workers()
                    worker_manager.start_worker(
                        worker, self.iface, "Starting export task..."
                    )

                else:
                    QMessageBox.warning(
                        None,
                        self.tr("WARNING!"),
                        self.tr("The selected directory does not exist!"),
                    )

            except Exception as z:
                QMessageBox.critical(None, "ERROR!", 'Error:\n"' + str(z) + '"')

    def validate_input(self):
        root = QgsProject.instance().layerTreeRoot()
        cle_group = root.findGroup("CLE")

        if cle_group:
            self.button_box.setEnabled(os.path.exists(self.dir_output.text()))

    def tr(self, message):
        return QCoreApplication.translate('ReportGen', message)
