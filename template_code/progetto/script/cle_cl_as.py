# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:		cle_cl_as.py
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


def cl_as(dialog, layer, feature):
    #data_as = dialog.findChild(QgsDateTimeEdit,"data_as")
    #today = QDate.currentDate()
    # data_as.setDate(today)
    sezione = find_child(dialog, QLineEdit, "sezione")
    ID_aggr = find_child(dialog, QLineEdit, "ID_aggr")
    ID_area = find_child(dialog, QLineEdit, "ID_area")
    ID_infra_a = find_child(dialog, QLineEdit, "ID_infra_a")
    ID_infra_b = find_child(dialog, QLineEdit, "ID_infra_b")
    ID_infra_c = find_child(dialog, QLineEdit, "ID_infra_c")
    ID_infra_d = find_child(dialog, QLineEdit, "ID_infra_d")
    n_unita = find_child(dialog, QLineEdit, "n_unita")
    n_edif = find_child(dialog, QLineEdit, "n_edif")
    n_edif_gl = find_child(dialog, QLineEdit, "n_edif_gl")
    n_murat = find_child(dialog, QLineEdit, "n_murat")
    n_ca = find_child(dialog, QLineEdit, "n_ca")
    n_altre = find_child(dialog, QLineEdit, "n_altre")
    altezza = find_child(dialog, QLineEdit, "altezza")
    superf = find_child(dialog, QLineEdit, "superf")
    piani_min = find_child(dialog, QLineEdit, "piani_min")
    piani_max = find_child(dialog, QLineEdit, "piani_max")
    lungh_fron = find_child(dialog, QLineEdit, "lungh_fron")
    us_interf = find_child(dialog, QLineEdit, "us_interf")
    zona_ms = find_child(dialog, QComboBox, "zona_ms")
    inst_name = find_child(dialog, QLabel, "inst_name")
    inst_fran = find_child(dialog, QCheckBox, "inst_fran")
    inst_liq = find_child(dialog, QCheckBox, "inst_liq")
    inst_fag = find_child(dialog, QCheckBox, "inst_fag")
    inst_ced = find_child(dialog, QCheckBox, "inst_ced")
    inst_cav = find_child(dialog, QCheckBox, "inst_cav")
    localita = find_child(dialog, QComboBox, "localita")
    cod_local = find_child(dialog, QLineEdit, "cod_local")
    conn_volte = find_child(dialog, QComboBox, "conn_volte")
    conn_rifus = find_child(dialog, QComboBox, "conn_rifus")
    regol_1 = find_child(dialog, QComboBox, "regol_1")
    regol_2 = find_child(dialog, QComboBox, "regol_2")
    regol_3 = find_child(dialog, QComboBox, "regol_3")
    regol_4 = find_child(dialog, QComboBox, "regol_4")
    regol_5 = find_child(dialog, QComboBox, "regol_5")
    vuln_1 = find_child(dialog, QComboBox, "vuln_1")
    vuln_2 = find_child(dialog, QComboBox, "vuln_2")
    vuln_3 = find_child(dialog, QComboBox, "vuln_3")
    vuln_4 = find_child(dialog, QComboBox, "vuln_4")
    vuln_5 = find_child(dialog, QComboBox, "vuln_5")
    vuln_6 = find_child(dialog, QComboBox, "vuln_6")
    vuln_6 = find_child(dialog, QComboBox, "vuln_6")
    rinfor_1 = find_child(dialog, QComboBox, "rinfor_1")
    rinfor_2 = find_child(dialog, QComboBox, "rinfor_2")
    morf = find_child(dialog, QComboBox, "morf")
    alluvio = find_child(dialog, QComboBox, "alluvio")
    alert_as = find_child(dialog, QLabel, "text_alert_as")
    alert_ae = find_child(dialog, QLabel, "text_alert_ae")
    alert_ac = find_child(dialog, QLabel, "text_alert_ac")

    alert_as.hide()
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
    validate_callback = partial(validateForm, button_box, dialog)

    ID_aggr.textEdited.connect(validate_callback)
    n_unita.textEdited.connect(validate_callback)
    n_edif.textEdited.connect(validate_callback)
    altezza.textEdited.connect(validate_callback)
    superf.textEdited.connect(validate_callback)
    piani_min.textEdited.connect(validate_callback)
    piani_max.textEdited.connect(validate_callback)
    lungh_fron.textEdited.connect(validate_callback)
    us_interf.textEdited.connect(validate_callback)
    conn_volte.currentIndexChanged.connect(
        validate_callback)
    conn_rifus.currentIndexChanged.connect(
        validate_callback)
    regol_1.currentIndexChanged.connect(
        validate_callback)
    regol_2.currentIndexChanged.connect(
        validate_callback)
    regol_3.currentIndexChanged.connect(
        validate_callback)
    regol_4.currentIndexChanged.connect(
        validate_callback)
    regol_5.currentIndexChanged.connect(
        validate_callback)
    vuln_1.currentIndexChanged.connect(
        validate_callback)
    vuln_2.currentIndexChanged.connect(
        validate_callback)
    vuln_3.currentIndexChanged.connect(
        validate_callback)
    vuln_4.currentIndexChanged.connect(
        validate_callback)
    vuln_5.currentIndexChanged.connect(
        validate_callback)
    vuln_6.currentIndexChanged.connect(
        validate_callback)
    rinfor_1.currentIndexChanged.connect(
        validate_callback)
    rinfor_2.currentIndexChanged.connect(
        validate_callback)
    morf.currentIndexChanged.connect(
        validate_callback)
    alluvio.currentIndexChanged.connect(
        validate_callback)
    ID_area.editingFinished.connect(validate_callback)
    ID_infra_a.editingFinished.connect(validate_callback)
    ID_infra_b.editingFinished.connect(validate_callback)
    ID_infra_c.editingFinished.connect(validate_callback)
    ID_infra_d.editingFinished.connect(validate_callback)
    n_murat.textEdited.connect(validate_callback)
    n_ca.textEdited.connect(validate_callback)
    n_altre.textEdited.connect(validate_callback)
    localita.currentIndexChanged.connect(
        partial(update_localita, dialog, cod_local, localita))
    sezione.textEdited.connect(partial(update_valore, sezione))
    ID_aggr.editingFinished.connect(
        partial(zero_digit, ID_aggr, alert_as, 10, 1))
    ID_area.editingFinished.connect(
        partial(zero_digit, ID_area, alert_ae, 10, 0))
    ID_infra_a.editingFinished.connect(
        partial(zero_digit, ID_infra_a, alert_ac, 10, 0))
    ID_infra_b.editingFinished.connect(
        partial(zero_digit, ID_infra_b, alert_ac, 10, 0))
    ID_infra_c.editingFinished.connect(
        partial(zero_digit, ID_infra_c, alert_ac, 10, 0))
    ID_infra_d.editingFinished.connect(
        partial(zero_digit, ID_infra_d, alert_ac, 10, 0))
    n_unita.textEdited.connect(partial(update_valore, n_unita))
    n_edif.textEdited.connect(partial(update_valore, n_edif))
    n_edif_gl.textEdited.connect(partial(update_valore, n_edif_gl))
    n_murat.textEdited.connect(partial(update_valore, n_murat))
    n_ca.textEdited.connect(partial(update_valore, n_ca))
    n_altre.textEdited.connect(partial(update_valore, n_altre))
    altezza.textEdited.connect(partial(update_valore, altezza))
    superf.textEdited.connect(partial(update_valore, superf))
    piani_min.textEdited.connect(partial(update_valore, piani_min))
    piani_max.textEdited.connect(partial(update_valore, piani_max))
    lungh_fron.textEdited.connect(partial(update_valore, lungh_fron))
    us_interf.textEdited.connect(partial(update_valore, us_interf))

    n_unita.textChanged.connect(validate_callback)
    n_edif.textChanged.connect(validate_callback)
    n_edif_gl.textChanged.connect(validate_callback)
    n_unita.textChanged.connect(validate_callback)
    n_murat.textChanged.connect(validate_callback)
    n_ca.textChanged.connect(validate_callback)
    n_altre.textChanged.connect(validate_callback)
    piani_min.textChanged.connect(validate_callback)
    piani_max.textChanged.connect(validate_callback)

    zona_ms.currentIndexChanged.connect(partial(disableInstab, dialog))

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
                find_child(dialog, QLineEdit, fld).setText(comuni_info[idx])
        except Exception as ex:
            QgsMessageLog.logMessage(
                'Error setting ISAT coded: %s' % ex, 'CLETools')

    # Set area from feature
    area = str(int(feature.geometry().area()))
    superf.setText(area)

    validate_callback()


def field_text(dialog, field_name):
    """Returns current field value"""

    try:
        try:
            return find_child(dialog, QComboBox, field_name).currentText()
        except:
            return find_child(dialog, QLineEdit, field_name).text()
    except:
        QgsMessageLog.logMessage(
            'Error looking for form field %s' % field_name, 'CLETools')
        return None


def field_int_val(dialog, field_name):
    """Returns int value or 0 of the given field_name"""

    try:
        return int(field_text(dialog, field_name))
    except:
        return 0


def validateForm(button_box, dialog, *args):
    """Form validator"""

    find_child(dialog, QLabel, 'error_text').setText('')
    find_child(dialog, QGroupBox, 'message_box').hide()
    for label in dialog.findChildren((QLabel, QCheckBox)):
        label.setStyleSheet('')

    # Map of field names -> field number
    REQUIRED_FIELDS = {
        'altezza': 16,
        'superf': 17,
        'piani_min': 18,
        'piani_max': 19,
        'lungh_fron': 20,
        'conn_volte': 22,
        'conn_rifus': 23,
        'regol_1': 24,
        'regol_2': 25,
        'regol_3': 26,
        'regol_4': 27,
        'regol_5': 28,
        'vuln_1': 29,
        'vuln_2': 31,
        'vuln_3': 32,
        'vuln_4': 33,
        'vuln_5': 34,
        'vuln_6': 35,
        'rinfor_1': 36,
        'rinfor_2': 37,
        'alluvio': 50,
    }

    errors = set()

    # Check required
    for field_name, field_index in REQUIRED_FIELDS.items():
        if not field_text(dialog, field_name):
            errors.add('Campo %s: obbigatorio!' % field_index)

    # Special rules
    if len(field_text(dialog, 'ID_aggr')) != 12:
        errors.add(
            'Campo 6: e\' obbligatorio e deve essere lungo esattamente 12 caratteri!')
    else:
        try:
            if int(field_text(dialog, 'ID_aggr')) == 0:
                errors.add('Campo 6: deve essere maggiore di zero!')
        except:
            errors.add('Campo 6: deve essere un numero valido!')

    # one of 7 8
    text_7 = field_text(dialog, 'ID_area')
    is_7_set = len(text_7) > 0
    if is_7_set:
        try:
            if int(text_7) == 0:
                errors.add('Campo 7: deve essere maggiore di zero!')
        except:
            errors.add('Campo 7: deve essere un numero valido!')

    # one of 6 a-d
    is_8_set = False
    i = 0
    infra_fields = ('ID_infra_a', 'ID_infra_b', 'ID_infra_c', 'ID_infra_d')
    for field_name in infra_fields:
        field_index = '8%s' % ['a', 'b', 'c', 'd'][i]
        text = field_text(dialog, field_name)
        if text:
            is_8_set = True
            try:
                if int(text) == 0:
                    errors.add('Campo 8: deve essere maggiore di zero!')
                if len(text) > 10:
                    errors.add(
                        'Campo 8: deve essere lungo esattamente 10 caratteri!')
            except:
                errors.add('Campo 8: deve essere un numero valido!')
            break

        i += 1

    if not is_7_set and not is_8_set:
        errors.add(
            'Campo 7: questo campo oppure il campo 8 devono essere compilati!')
        errors.add(
            'Campo 8: questo campo oppure il campo 7 devono essere compilati!')

    # 10 required and must be >= 2
    try:
        int_10 = int(field_text(dialog, 'n_unita'))
    except:
        errors.add('Campo 10: deve essere un numero valido!')
        int_10 = 0

    try:
        int_11 = int(field_text(dialog, 'n_edif'))
    except:
        errors.add('Campo 11: deve essere un numero valido!')
        int_11 = 0

    if int_10 < 2:
        errors.add('Campo 10: e\' obbligatorio e deve essere >= 2!')

    if int_11 > int_10:
        errors.add(
            'Campo 11: non puo\' essere maggiore del valore del campo 10!')

    # one of 13-15
    numero_us = ('n_murat', 'n_ca', 'n_altre')
    i = 0
    int_val = 0
    for field_name in numero_us:
        try:
            int_val += int(field_text(dialog, field_name))
        except:
            errors.add(
                'Campo %s: deve essere un numero valido!' % (i + 13))
        i += 1

    if int_val == 0:
        errors.add('Campo 13: almeno uno dei campi 13-15 e\' obbligatorio!')

    # 21 is required if 20 is > 0
    try:
        int_20 = int(field_text(dialog, 'lungh_fron'))
    except:
        int_20 = 0

    try:
        int_21 = int(field_text(dialog, 'us_interf'))
    except:
        int_21 = 0

    if int_20 > 0 and int_21 == 0:
        errors.add(
            'Campo 21: obbligatorio perche\' il campo 20 e\' maggiore di zero!')

    if is_8_set and int_20 <= 0:
        errors.add(
            'Campo 20: deve essere un numero maggiore di zero perche\' il campo 8 e\' compilato!')

    if is_8_set and int_21 <= 0:
        errors.add(
            'Campo 21: deve essere un numero maggiore di zero perche\' il campo 8 e\' compilato!')

    # 41-45 required if 40 == 3
    if field_text(dialog, 'zona_ms') == "3 - Instabile":
        is_set = False
        for field_name in ('inst_fran', 'inst_liq', 'inst_fag', 'inst_ced', 'inst_cav'):
            if find_child(dialog, QCheckBox, field_name).isChecked():
                is_set = True
                break

        if not is_set:
            errors.add(
                'Campo 41-45: selezionare almeno un tipo di instabilita\'!')

    if field_int_val(dialog, 'altezza') <= 0:
        errors.add('Campo 16: deve essere un numero valido maggiore di zero!')

    if field_int_val(dialog, 'piani_min') <= 0:
        errors.add('Campo 18: deve essere un numero valido maggiore di zero!')

    if field_int_val(dialog, 'piani_max') <= 0:
        errors.add('Campo 19: deve essere un numero valido maggiore di zero!')

    # Check
    n_unita = field_int_val(dialog, "n_unita")  # 10
    n_edif = field_int_val(dialog, "n_edif")  # 11
    n_edif_gl = field_int_val(dialog, "n_edif_gl")  # 12

    if n_edif > n_unita:
        errors.add('Campo 11: non puo\' essere maggiore del valore del campo 10!')

    if n_edif_gl > n_unita:
        errors.add('Campo 12: non puo\' essere maggiore del valore del campo 10!')

    n_murat = field_int_val(dialog, "n_murat")
    n_ca = field_int_val(dialog, "n_ca")
    n_altre = field_int_val(dialog, "n_altre")

    if n_unita != n_ca + n_altre + n_murat:
        errors.add(
            'Campo 10: deve essere uguale alla somma dei valori dei campi 13, 14 e 15!')

    piani_min = field_int_val(dialog, "piani_min")
    piani_max = field_int_val(dialog, "piani_max")

    if piani_min > piani_max:
        errors.add(
            'Campo 18: deve essere inferiore al valore del campo 19!')

    if len(errors) > 0:

        errors = list(errors)
        errors.sort(key=lambda msg: int(
            re.match(r'^Campo (\d+)[a-f]?', msg).groups()[0]))

        find_child(dialog, QGroupBox, 'message_box').show()
        find_child(dialog, QLabel, 'error_text').setText(
            '<p style="color:red">' + '<br>'.join(errors) + '</p>')

        for error_message in errors:
            match = re.match(r'^Campo ([\d]+[a-f]?)', error_message)
            if match:
                field_index = match.groups()[0]
                set_label_error(dialog, field_index)

    button_box.setEnabled(len(errors) == 0)


def zero_digit(campo, alert, max_digits, add_00):
    if campo.text():
        length = len(campo.text()) - add_00 * 2
        if length != max_digits:
            if length < max_digits:
                diff = max_digits - length
                if add_00 == 0:
                    text = ('0'*diff) + campo.text()
                elif add_00 == 1:
                    text = ('0'*(diff-2)) + campo.text() + '00'
                campo.setText(text)
                alert.hide()
            # elif length > max_digits:
            #    alert.show()


def update_valore(value):
    value.setText(re.sub('[^0-9]', '', value.text()))


############################################
# Disabled: now implemented in the validator
if False:
    def alert_us_1(dialog):
        n_unita = find_child(dialog, QLineEdit, "n_unita")
        n_edif = find_child(dialog, QLineEdit, "n_edif")
        n_edif_gl = find_child(dialog, QLineEdit, "n_edif_gl")
        if (n_unita.text() != '') and (n_edif.text() != ''):
            if int(n_edif.text()) > int(n_unita.text()):
                QMessageBox.warning(
                    None, 'WARNING!', "The value of the '11 NUMERO US CON FUNZIONI STRATEGICHE' field is greater than the value of the '10 NUMERO TOTALI UNITA' STRUTTURALI' field!")
                n_edif.setText('')
                n_unita.setText('')
        if (n_unita.text() != '') and (n_edif_gl.text() != ''):
            if int(n_edif_gl.text()) > int(n_unita.text()):
                QMessageBox.warning(
                    None, 'WARNING!', "The value of the '12 NUMERO US CARATTERIZZATE DA GRANDI LUCI' field is greater than the value of the '10 NUMERO TOTALI UNITA' STRUTTURALI' field!")
                n_edif_gl.setText('')
                n_unita.setText('')

    def alert_us_2(dialog):
        n_unita = find_child(dialog, QLineEdit, "n_unita")
        n_murat = find_child(dialog, QLineEdit, "n_murat")
        n_ca = find_child(dialog, QLineEdit, "n_ca")
        n_altre = find_child(dialog, QLineEdit, "n_altre")
        if (n_unita.text() != '') and (n_murat.text() != '') and (n_ca.text() != '') and (n_altre.text() != ''):
            if not int(n_unita.text()) == int(n_murat.text()) + int(n_ca.text()) + int(n_altre.text()):
                QMessageBox.warning(
                    None, 'WARNING!', "The value of '10 NUMERO TOTALI UNITA' STRUTTURALI' must be equal to the sum of '13 MURATURA', '14 C.A.' and '15 ALTRE STRUTTURE' field!")
                n_murat.setText('')
                n_ca.setText('')
                n_altre.setText('')

    def alert_us_3(dialog):
        piani_min = find_child(dialog, QLineEdit, "piani_min")
        piani_max = find_child(dialog, QLineEdit, "piani_max")
        if (piani_min.text() == '') and (piani_max.text() == ''):
            pass
        elif (piani_min.text() != '') and (piani_max.text() != ''):
            if int(piani_min.text()) > int(piani_max.text()):
                QMessageBox.warning(
                    None, 'WARNING!', "The value of the '18 NUMERI PIANI MINIMO' field is greater than the value of the '19 NUMERO PIANI MASSIMO' field!")
                piani_min.setText('')
                piani_max.setText('')


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
