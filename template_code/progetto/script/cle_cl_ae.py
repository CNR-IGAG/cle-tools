# coding=utf-8
# -------------------------------------------------------------------------------
# Name:		cle_cl_ae.py
# Author:	  Tarquini E.
# Created:	 22-09-2018
# -------------------------------------------------------------------------------

import re
import webbrowser


from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.utils import *

from functools import partial


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


def cl_ae(dialog, layer, feature):
    #data_ae = dialog.findChild(QgsDateTimeEdit,"data_ae")
    #today = QDate.currentDate()
    # data_ae.setDate(today)
    ID_area = find_child(dialog, QLineEdit, "ID_area")
    ID_infra_a = find_child(dialog, QLineEdit, "ID_infra_a")
    ID_infra_b = find_child(dialog, QLineEdit, "ID_infra_b")
    ID_infra_c = find_child(dialog, QLineEdit, "ID_infra_c")
    ID_infra_d = find_child(dialog, QLineEdit, "ID_infra_d")
    denom = find_child(dialog, QLineEdit, "denom")
    anno_piano = find_child(dialog, QLineEdit, "anno_piano")
    n_aggreg = find_child(dialog, QLineEdit, "n_aggreg")
    n_manuf = find_child(dialog, QLineEdit, "n_manuf")
    superf = find_child(dialog, QLineEdit, "superf")
    rett_max = find_child(dialog, QLineEdit, "rett_max")
    rett_min = find_child(dialog, QLineEdit, "rett_min")
    zona_ms = find_child(dialog, QComboBox, "zona_ms")
    inst_name = find_child(dialog, QLabel, "inst_name")
    inst_fran = find_child(dialog, QCheckBox, "inst_fran")
    inst_liq = find_child(dialog, QCheckBox, "inst_liq")
    inst_fag = find_child(dialog, QCheckBox, "inst_fag")
    inst_ced = find_child(dialog, QCheckBox, "inst_ced")
    inst_cav = find_child(dialog, QCheckBox, "inst_cav")
    localita = find_child(dialog, QComboBox, "localita")
    cod_local = find_child(dialog, QLineEdit, "cod_local")
    tipo_area = find_child(dialog, QComboBox, "tipo_area")
    piano = find_child(dialog, QComboBox, "piano")
    pav_per = find_child(dialog, QComboBox, "pav_per")
    infra_acq = find_child(dialog, QComboBox, "infra_acq")
    infra_ele = find_child(dialog, QComboBox, "infra_ele")
    infra_fog = find_child(dialog, QComboBox, "infra_fog")
    morf = find_child(dialog, QComboBox, "morf")
    falda = find_child(dialog, QComboBox, "falda")
    acq_sup = find_child(dialog, QComboBox, "acq_sup")
    alluvio = find_child(dialog, QComboBox, "alluvio")
    alert_ae = find_child(dialog, QLabel, "text_alert_ae")
    alert_ac = find_child(dialog, QLabel, "text_alert_ac")

    alert_ae.hide()
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

    button_box.setEnabled(False)

    ID_area.textChanged.connect(validation_callback)
    localita.currentIndexChanged.connect(
        validation_callback)
    denom.textEdited.connect(validation_callback)
    tipo_area.currentIndexChanged.connect(
        validation_callback)
    piano.currentIndexChanged.connect(
        validation_callback)
    anno_piano.textEdited.connect(validation_callback)
    n_aggreg.textEdited.connect(validation_callback)
    n_manuf.textEdited.connect(validation_callback)
    superf.textEdited.connect(validation_callback)
    rett_max.textEdited.connect(validation_callback)
    rett_min.textEdited.connect(validation_callback)
    pav_per.currentIndexChanged.connect(
        validation_callback)
    infra_acq.currentIndexChanged.connect(
        validation_callback)
    infra_ele.currentIndexChanged.connect(
        validation_callback)
    infra_fog.currentIndexChanged.connect(
        validation_callback)
    morf.currentIndexChanged.connect(
        validation_callback)
    falda.currentIndexChanged.connect(
        validation_callback)
    acq_sup.currentIndexChanged.connect(
        validation_callback)
    alluvio.currentIndexChanged.connect(
        validation_callback)
    ID_infra_a.textEdited.connect(validation_callback)
    ID_infra_b.textEdited.connect(validation_callback)
    ID_infra_c.textEdited.connect(validation_callback)
    ID_infra_d.textEdited.connect(validation_callback)
    localita.currentIndexChanged.connect(
        partial(update_localita, dialog, cod_local, localita))
    ID_area.editingFinished.connect(partial(zero_digit, ID_area, alert_ae, 10))
    ID_infra_a.editingFinished.connect(
        partial(zero_digit, ID_infra_a, alert_ac, 10))
    ID_infra_b.editingFinished.connect(
        partial(zero_digit, ID_infra_b, alert_ac, 10))
    ID_infra_c.editingFinished.connect(
        partial(zero_digit, ID_infra_c, alert_ac, 10))
    ID_infra_d.editingFinished.connect(
        partial(zero_digit, ID_infra_d, alert_ac, 10))
    anno_piano.textEdited.connect(partial(update_valore, anno_piano))
    n_aggreg.textEdited.connect(partial(update_valore, n_aggreg))
    n_manuf.textEdited.connect(partial(update_valore, n_manuf))
    superf.textEdited.connect(partial(update_valore, superf))
    rett_max.textEdited.connect(partial(update_valore, rett_max))
    rett_min.textEdited.connect(partial(update_valore, rett_min))
    rett_max.editingFinished.connect(partial(alert_area, dialog))
    rett_min.editingFinished.connect(partial(alert_area, dialog))
    superf.editingFinished.connect(partial(alert_area_2, dialog))
    zona_ms.currentIndexChanged.connect(partial(disableInstab, dialog))
    zona_ms.currentIndexChanged.connect(validation_callback)

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
                'Error setting ISAT coded: %s' % ex, 'CLETools')

    # Set area from feature
    area = str(int(feature.geometry().area()))
    superf.setText(area)


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

    find_child(dialog, QLabel, 'error_text').setText('')
    find_child(dialog, QGroupBox, 'message_box').hide()

    for label in dialog.findChildren((QLabel, QCheckBox)):
        label.setStyleSheet('')

    # Map of field names -> field number
    REQUIRED_FIELDS = {
        'ID_area': 5,
        'denom': 7,
        'tipo_area': 8,
        'piano': 9,
        'anno_piano': 10,
        'n_aggreg': 11,
        'n_manuf': 12,
        'superf': 13,
        'rett_max': 14,
        'rett_min': 15,
        'pav_per': 16,
        'infra_acq': 17,
        'infra_ele': 18,
        'infra_fog': 19,
        'morf': 20,
        'falda': 32,
        'acq_sup': 33,
        'alluvio': 35,
    }

    errors = {}

    # Check required
    for field_name, field_index in REQUIRED_FIELDS.items():
        if not field_text(dialog, field_name):
            errors[field_name] = 'Campo %s: obbigatorio!' % field_index

    # Special rules
    if len(field_text(dialog, 'ID_area')) != 10:
        errors['ID_area'] = 'Campo 5: e\' obbligatorio e deve essere lungo esattamente 10 caratteri!'
    else:
        try:
            if int(field_text(dialog, 'ID_area')) == 0:
                errors['ID_area'] = 'Campo 5: deve essere maggiore di zero!'
        except:
            errors['ID_area'] = 'Campo 5: deve essere un numero valido!'

    # one of 6 a-d
    is_set = False
    i = 0
    infra_fields = ('ID_infra_a', 'ID_infra_b', 'ID_infra_c', 'ID_infra_d')
    for field_name in infra_fields:
        field_index = '6%s' % ['a', 'b', 'c', 'd'][i]
        text = field_text(dialog, field_name)
        if text:
            is_set = True
            try:
                if int(text) == 0:
                    errors[field_name] = 'Campo 6: deve essere maggiore di zero!'
                if len(text) > 10:
                    errors[field_name] = 'Campo 6: deve essere lungo esattamente 10 caratteri!'
            except:
                errors[field_name] = 'Campo 6: deve essere un numero valido!'
            break

        i += 1

    if not is_set:
        errors['ID_infra_a'] = 'Campo 6: deve contenere almeno un identificativo di infrastruttura diverso da zero!'

    # 24-28 required if 23 == 3
    if field_text(dialog, 'zona_ms') == "3 - Instabile":
        is_set = False
        for field_name in ('inst_fran', 'inst_liq', 'inst_fag', 'inst_ced', 'inst_cav'):
            if dialog.findChild(QCheckBox, field_name).isChecked():
                is_set = True
                break

        if not is_set:
            errors['inst_fran'] = 'Campo 24-28: almeno un tipo di instabilita\' deve essere selezionato!'

    if not validate_not_zero(dialog, 'rett_max'):
        errors['rett_max'] = 'Campo 14: deve essere un numero valido maggiore di zero!'

    if not validate_not_zero(dialog, 'rett_min'):
        errors['rett_min'] = 'Campo 15: deve essere un numero valido maggiore di zero!'

    if len(errors) > 0:
        find_child(dialog, QGroupBox, 'message_box').show()
        find_child(dialog, QLabel, 'error_text').setText(
            '<p style="color:red">' + '<br>'.join(list(errors.values())) + '</p>')

        for error_message in list(errors.values()):
            match = re.match(r'^Campo ([\d]+[a-f]?)', error_message)
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


def alert_area(dialog):
    rett_max = find_child(dialog, QLineEdit, "rett_max")
    rett_min = find_child(dialog, QLineEdit, "rett_min")
    if (rett_max.text() != '') and (rett_min.text() != ''):
        if int(rett_min.text()) > int(rett_max.text()):
            QMessageBox.warning(
                None, 'WARNING!', "Il valore del campo '15 MINIMA' e\' maggiore del valore del campo '14 MASSIMA'!")
            rett_min.setText('')
            rett_max.setText('')


def alert_area_2(dialog):
    rett_max = find_child(dialog, QLineEdit, "rett_max")
    rett_min = find_child(dialog, QLineEdit, "rett_min")
    superf = find_child(dialog, QLineEdit, "superf")
    if (rett_max.text() != '') and (rett_min.text() != '') and (superf.text() != ''):
        if int(superf.text()) < int(rett_max.text())*int(rett_min.text()):
            QMessageBox.warning(
                None, 'WARNING!', "Il prodotto del campo '14 MASSIMA' per il campo '15 MINIMA' e\' maggiore del valore del campo '13 SUPERFICIE DELL''AREA' field!")
            rett_min.setText('')
            rett_max.setText('')
            superf.setText('')


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
