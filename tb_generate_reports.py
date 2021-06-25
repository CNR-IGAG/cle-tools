import os

from qgis.core import *
from qgis.core import QgsMessageLog
from qgis.gui import *
from qgis.PyQt import uic
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.utils import *

from . import constants
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

        self.help_button.setEnabled(False)  # to delete
        self.dir_output.clear()
        self.alert_text.hide()
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
                raise z
                QMessageBox.critical(None, "ERROR!", 'Error:\n"' + str(z) + '"')

    def validate_input(self):
        if os.path.exists(self.dir_output.text()):
            self.button_box.setEnabled(True)