# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:		cle_cl_ac.py
# Author:	  Tarquini E.
# Created:	 22-09-2018
# -------------------------------------------------------------------------------

import re
import webbrowser
from functools import partial

from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.utils import *


LABEL_CACHE = {}

WIDGET_CACHE = {}


def find_child(dialog, typ, name):
    global WIDGET_CACHE

    try:
        return WIDGET_CACHE[name]
    except KeyError:
        WIDGET_CACHE[name] = dialog.findChild(typ, name)
        return WIDGET_CACHE[name]


def set_label_error(dialog, field_index):
    global LABEL_CACHE

    if len(LABEL_CACHE) == 0:
        LABEL_CACHE = dialog.findChildren((QLabel, QCheckBox))

    for label in LABEL_CACHE:
        if label.text().startswith(field_index + ' '):
            label.setStyleSheet('* {color: red;}')
            break


def cl_ac(dialog, layer, feature):
    ID_infra = find_child(dialog, QLineEdit, "ID_infra")
    #data_ac = dialog.findChild(QgsDateTimeEdit,"data_ac")
    #today = QDate.currentDate()
    # data_ac.setDate(today)
    largh_max = find_child(dialog, QLineEdit, "largh_max")
    largh_min = find_child(dialog, QLineEdit, "largh_min")
    lungh = find_child(dialog, QLineEdit, "lungh")
    lungh_vuo = find_child(dialog, QLineEdit, "lungh_vuo")
    n_aggreg = find_child(dialog, QLineEdit, "n_aggreg")
    n_manuf = find_child(dialog, QLineEdit, "n_manuf")
    el_ferrov = find_child(dialog, QLineEdit, "el_ferrov")
    el_pont = find_child(dialog, QLineEdit, "el_pont")
    el_tunn = find_child(dialog, QLineEdit, "el_tunn")
    el_pont_at = find_child(dialog, QLineEdit, "el_pont_at")
    el_muri = find_child(dialog, QLineEdit, "el_muri")
    pendenza = find_child(dialog, QLineEdit, "pendenza")
    zona_ms = find_child(dialog, QComboBox, "zona_ms")
    inst_name = find_child(dialog, QLabel, "inst_name")
    inst_fran = find_child(dialog, QCheckBox, "inst_fran")
    inst_liq = find_child(dialog, QCheckBox, "inst_liq")
    inst_fag = find_child(dialog, QCheckBox, "inst_fag")
    inst_ced = find_child(dialog, QCheckBox, "inst_ced")
    inst_cav = find_child(dialog, QCheckBox, "inst_cav")
    tipo_infra = find_child(dialog, QComboBox, "tipo_infra")
    localita = find_child(dialog, QComboBox, "localita")
    cod_local = find_child(dialog, QLineEdit, "cod_local")
    pav_per = find_child(dialog, QComboBox, "pav_per")
    ost_disc = find_child(dialog, QComboBox, "ost_disc")
    morf = find_child(dialog, QComboBox, "morf")
    acq_sup = find_child(dialog, QComboBox, "acq_sup")
    alluvio = find_child(dialog, QComboBox, "alluvio")
    strade_a = find_child(dialog, QCheckBox, "strade_a")
    strade_b = find_child(dialog, QCheckBox, "strade_b")
    strade_c = find_child(dialog, QCheckBox, "strade_c")
    strade_d = find_child(dialog, QCheckBox, "strade_d")
    strade_e = find_child(dialog, QCheckBox, "strade_e")
    strade_f = find_child(dialog, QCheckBox, "strade_f")
    alert_ac = find_child(dialog, QLabel, "text_alert_ac")

    alert_ac.hide()
    inst_name.hide()
    inst_fran.hide()
    inst_liq.hide()
    inst_fag.hide()
    inst_ced.hide()
    inst_cav.hide()

    help_button = find_child(dialog, QPushButton, "help_button")
    help_button.clicked.connect(partial(webbrowser.open,
                                        'https://www.youtube.com/watch?v=drs3COLtML8'))
    help_button.setEnabled(False)  # to delete

    button_box = find_child(dialog, QDialogButtonBox, "button_box")

    validation_callback = partial(form_validator, button_box, dialog)

    ID_infra.textChanged.connect(validation_callback)
    largh_max.textEdited.connect(validation_callback)
    largh_min.textEdited.connect(validation_callback)
    localita.currentIndexChanged.connect(
        validation_callback)
    tipo_infra.currentIndexChanged.connect(
        validation_callback)
    lungh.textChanged.connect(validation_callback)
    lungh_vuo.textChanged.connect(validation_callback)
    pav_per.currentTextChanged.connect(
        validation_callback)
    ost_disc.currentTextChanged.connect(
        validation_callback)
    n_aggreg.textChanged.connect(validation_callback)
    n_manuf.textChanged.connect(validation_callback)
    pendenza.textChanged.connect(validation_callback)
    morf.currentIndexChanged.connect(validation_callback)
    acq_sup.currentIndexChanged.connect(
        validation_callback)
    alluvio.currentIndexChanged.connect(
        validation_callback)
    strade_a.stateChanged.connect(validation_callback)
    strade_b.stateChanged.connect(validation_callback)
    strade_c.stateChanged.connect(validation_callback)
    strade_d.stateChanged.connect(validation_callback)
    strade_e.stateChanged.connect(validation_callback)
    strade_f.stateChanged.connect(validation_callback)

    inst_cav.stateChanged.connect(validation_callback)
    inst_ced.stateChanged.connect(validation_callback)
    inst_fag.stateChanged.connect(validation_callback)
    inst_fran.stateChanged.connect(validation_callback)
    inst_liq.stateChanged.connect(validation_callback)

    localita.currentIndexChanged.connect(
        partial(update_localita, dialog, cod_local, localita))
    ID_infra.editingFinished.connect(
        partial(zero_digit, ID_infra, alert_ac, 10))
    largh_max.textEdited.connect(partial(update_valore, largh_max))
    largh_min.textEdited.connect(partial(update_valore, largh_min))
    lungh.textEdited.connect(partial(update_valore, lungh))
    lungh_vuo.textEdited.connect(partial(update_valore, lungh_vuo))
    n_aggreg.textEdited.connect(partial(update_valore, n_aggreg))
    n_manuf.textEdited.connect(partial(update_valore, n_manuf))
    el_ferrov.textEdited.connect(partial(update_valore, el_ferrov))
    el_pont.textEdited.connect(partial(update_valore, el_pont))
    el_tunn.textEdited.connect(partial(update_valore, el_tunn))
    el_pont_at.textEdited.connect(partial(update_valore, el_pont_at))
    el_muri.textEdited.connect(partial(update_valore, el_muri))
    pendenza.textEdited.connect(partial(update_valore, pendenza))
    largh_max.editingFinished.connect(partial(alert_larg, dialog))
    largh_min.editingFinished.connect(partial(alert_larg, dialog))
    lungh.editingFinished.connect(partial(alert_larg_2, dialog))
    lungh_vuo.editingFinished.connect(partial(alert_larg_2, dialog))
    zona_ms.currentIndexChanged.connect(partial(disableInstab, dialog))
    zona_ms.currentIndexChanged.connect(validation_callback)

    # Set road length from feature
    length = str(int(feature.geometry().length()))
    lungh.setText(length)

    if lungh_vuo.text() == '0' or lungh_vuo.text() == '':
        lungh_vuo.setText(length)

    if find_child(dialog, QLineEdit, 'comune').text() == 'NULL':
        try:
            comuni = QgsProject.instance().mapLayersByName(
                'Limiti comunali')[0]
            comune = next(comuni.getFeatures(QgsFeatureRequest().setFilterExpression(
                'intersects($geometry, geom_from_wkt(\'%s\'))' % feature.geometry().asWkt())))
            comuni_info = dict(
                zip(comune.fields().names(), comune.attributes()))

            fields = {
                'cod_regio': 'cod_reg',
                'cod_prov': 'cod_prov',
                'cod_com': 'cod_com',
                'comune': 'comune',
                'provincia': 'provincia',
                'regione': 'regione'
            }
            for idx, fld in fields.items():
                dialog.findChild(QLineEdit, fld).setText(comuni_info[idx])
        except Exception as ex:
            QgsMessageLog.logMessage(
                'Error setting ISTAT coded: %s' % ex, 'CLETools')

    validation_callback()


def field_text(dialog, field_name):
    """Returns current field value"""

    try:
        try:
            return dialog.findChild(QComboBox, field_name).currentText()
        except:
            return dialog.findChild(QLineEdit, field_name).text()
    except:
        QgsMessageLog.logMessage(
            'Error looking for form field %s' % field_name, 'CLETools')
        return None


def validate_not_zero(dialog, field_name):
    """Validate a field is non zero and a valid number"""

    try:
        try:
            txt = dialog.findChild(QComboBox, field_name).currentText()
        except:
            txt = dialog.findChild(QLineEdit, field_name).text()
    except:
        QgsMessageLog.logMessage(
            'Error looking for form field %s' % field_name, 'CLETools')
        return False

    try:
        return int(txt) > 0
    except:
        return False


def form_validator(button_box, dialog):
    """Validation"""

    find_child(dialog, QLabel, 'error_text').setText('')
    find_child(dialog, QGroupBox, 'message_box').hide()
    for label in dialog.findChildren((QLabel, QCheckBox)):
        label.setStyleSheet('')

    # Map of field names -> field number
    REQUIRED_FIELDS = {
        'tipo_infra': 5,
        'ID_infra': 6,  # exact 10 chars
        'largh_max': 14,
        'largh_min': 15,
        'lungh': 16,
        'lungh_vuo': 17,
        'pav_per': 18,
        'ost_disc': 19,
        'n_aggreg': 20,  # 20: 0 is allowed
        'pendenza': 26,
        'morf': 27,
        'acq_sup': 40,
        'alluvio': 42,
    }

    errors = {}

    # Check required
    for field_name, field_index in REQUIRED_FIELDS.items():
        if not field_text(dialog, field_name):
            errors[field_name] = 'Campo %s: obbigatorio!' % field_index

    # Special rules

    # one of 8-13
    is_set = False
    for field_name in ('strade_a', 'strade_b', 'strade_c', 'strade_d', 'strade_e', 'strade_f'):
        if dialog.findChild(QCheckBox, field_name).isChecked():
            is_set = True
            break

    if not is_set:
        errors['strade_a'] = 'Campo 8-13: almeno un tipo di strada deve essere selezionato!'

    if not validate_not_zero(dialog, 'largh_max'):
        errors['largh_max'] = 'Campo 14: deve essere un numero maggiore di zero!'

    if not validate_not_zero(dialog, 'largh_min'):
        errors['largh_min'] = 'Campo 15: deve essere un numero maggiore di zero!'

    if len(field_text(dialog, 'ID_infra')) != 10:
        errors['ID_infra'] = 'Campo 6: deve essere lungo esattamente 10 caratteri!'
    else:
        try:
            if int(field_text(dialog, 'ID_infra')) == 0:
                errors['ID_infra'] = 'Campo 6: deve essere un numero maggiore di zero!'
        except:
            errors['ID_infra'] = 'Campo 6: deve essere un numero valido!'

    # 31-35 required if 30 == 3
    if field_text(dialog, 'zona_ms') == "3 - Instabile":
        is_set = False
        for field_name in ('inst_fran', 'inst_liq', 'inst_fag', 'inst_ced', 'inst_cav'):
            if dialog.findChild(QCheckBox, field_name).isChecked():
                is_set = True
                break

        if not is_set:
            errors['inst_fran'] = 'Campo 31-35: almeno un tipo di instabilita\' deve essere selezionato!'

    if len(errors) > 0:
        find_child(dialog, QGroupBox, 'message_box').show()
        find_child(dialog, QLabel, 'error_text').setText(
            '<p style="color:red">' + '<br>'.join(list(errors.values())) + '</p>')

        find_child(dialog, QGroupBox, 'message_box').adjustSize()

        for error_message in list(errors.values()):
            match = re.match(r'^Campo ([\d]+)', error_message)
            if match:
                field_index = match.groups()[0]
                set_label_error(dialog, field_index)

    button_box.setEnabled(len(errors) == 0)


def zero_digit(campo, alert, n):
    a = len(campo.text())
    if a > 0:
        if a < n:
            b = n - a
            c = ('0'*b) + campo.text()
            campo.setText(c)
            alert.hide()
        elif a > n:
            campo.setText("")
            alert.show()


def update_valore(value):
    value.setText(re.sub('[^0-9]', '', value.text()))


def alert_larg(dialog):
    largh_max = find_child(dialog, QLineEdit, "largh_max")
    largh_min = find_child(dialog, QLineEdit, "largh_min")
    if (largh_max.text() != '') and (largh_min.text() != ''):
        if int(largh_min.text()) > int(largh_max.text()):
            QMessageBox.warning(
                None, 'WARNING!', "Il valore del campo '15 MINIMA' e\' maggiore del valore del campo '14 MASSIMA'!")
            largh_min.setText('')
            largh_max.setText('')


def alert_larg_2(dialog):
    lungh = find_child(dialog, QLineEdit, "lungh")
    lungh_vuo = find_child(dialog, QLineEdit, "lungh_vuo")
    if (lungh.text() != '') and (lungh_vuo.text() != ''):
        if int(lungh_vuo.text()) > int(lungh.text()):
            QMessageBox.warning(
                None, 'WARNING!', "Il valore del campo '17 LUNGHEZZA TRATTO STRADALE SENZA AGGREGATIE UNITA' ISOLATE INTERFERENTI' e\' maggiore del valore del campo '16 LUNGHEZZA COMPLESSIVA'!")
            lungh_vuo.setText('')
            lungh.setText('')


def disableInstab(dialog):
    zona_ms = find_child(dialog, QComboBox, "zona_ms")
    inst_name = find_child(dialog, QLabel, "inst_name")
    inst_fran = find_child(dialog, QCheckBox, "inst_fran")
    inst_liq = find_child(dialog, QCheckBox, "inst_liq")
    inst_fag = find_child(dialog, QCheckBox, "inst_fag")
    inst_ced = find_child(dialog, QCheckBox, "inst_ced")
    inst_cav = find_child(dialog, QCheckBox, "inst_cav")
    if zona_ms.currentText() == "3 - Instabile":
        inst_name.show()
        inst_fran.show()
        inst_liq.show()
        inst_fag.show()
        inst_ced.show()
        inst_cav.show()
        inst_fran.setEnabled(True)
        inst_liq.setEnabled(True)
        inst_fag.setEnabled(True)
        inst_ced.setEnabled(True)
        inst_cav.setEnabled(True)
    else:
        inst_fran.setChecked(False)
        inst_fran.setEnabled(False)
        inst_liq.setChecked(False)
        inst_liq.setEnabled(False)
        inst_fag.setChecked(False)
        inst_fag.setEnabled(False)
        inst_ced.setChecked(False)
        inst_ced.setEnabled(False)
        inst_cav.setChecked(False)
        inst_cav.setEnabled(False)


def update_localita(dialog, cod_local, localita):
    localita = find_child(dialog, QComboBox, "localita")
    cod_local = find_child(dialog, QLineEdit, "cod_local")
    try:
        TipoIndagine = str(localita.currentText().strip()).split("  -  ")[1]
        cod_local.setText(TipoIndagine)
    except:
        pass
