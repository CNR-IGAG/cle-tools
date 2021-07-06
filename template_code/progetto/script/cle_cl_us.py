# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:		cle_cl_us.py
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


def set_label_error(dialog, field_index, message):
    global LABEL_CACHE

    if len(LABEL_CACHE) == 0:
        LABEL_CACHE = dialog.findChildren((QLabel, QCheckBox))

    for label in LABEL_CACHE:
        if label.text().startswith(field_index + ' '):
            label.setStyleSheet('* {color: red;}')
            break


def cl_us(dialog, layer, feature):
    #data_us = dialog.findChild(QgsDateTimeEdit,"data_us")
    #today = QDate.currentDate()
    # data_us.setDate(today)
    sezione = find_child(dialog, QLineEdit, "sezione")
    ID_aggr = find_child(dialog, QLineEdit, "ID_aggr")
    ID_unit = find_child(dialog, QLineEdit, "ID_unit")
    ID_area = find_child(dialog, QLineEdit, "ID_area")
    ID_infra_a = find_child(dialog, QLineEdit, "ID_infra_a")
    ID_infra_b = find_child(dialog, QLineEdit, "ID_infra_b")
    ID_infra_c = find_child(dialog, QLineEdit, "ID_infra_c")
    ID_infra_d = find_child(dialog, QLineEdit, "ID_infra_d")
    civico = find_child(dialog, QLineEdit, "civico")
    n_piani = find_child(dialog, QLineEdit, "n_piani")
    alt_totale = find_child(dialog, QLineEdit, "alt_totale")
    superf_m = find_child(dialog, QLineEdit, "superf_m")
    zona_ms = find_child(dialog, QComboBox, "zona_ms")
    inst_name = find_child(dialog, QLabel, "inst_name")
    inst_fran = find_child(dialog, QCheckBox, "inst_fran")
    inst_liq = find_child(dialog, QCheckBox, "inst_liq")
    inst_fag = find_child(dialog, QCheckBox, "inst_fag")
    inst_ced = find_child(dialog, QCheckBox, "inst_ced")
    inst_cav = find_child(dialog, QCheckBox, "inst_cav")
    isolato = find_child(dialog, QComboBox, "isolato")
    posizio = find_child(dialog, QComboBox, "posizio")
    spec = find_child(dialog, QComboBox, "spec")
    specialis = find_child(dialog, QComboBox, "specialis")
    strutt_ver = find_child(dialog, QComboBox, "strutt_ver")
    tipo_mur = find_child(dialog, QComboBox, "tipo_mur")
    uso_a = find_child(dialog, QCheckBox, "uso_a")
    uso_a_1 = find_child(dialog, QLineEdit, "uso_a_1")
    uso_b = find_child(dialog, QCheckBox, "uso_b")
    uso_b_1 = find_child(dialog, QLineEdit, "uso_b_1")
    uso_c = find_child(dialog, QCheckBox, "uso_c")
    uso_c_1 = find_child(dialog, QLineEdit, "uso_c_1")
    uso_d = find_child(dialog, QCheckBox, "uso_d")
    uso_d_1 = find_child(dialog, QLineEdit, "uso_d_1")
    uso_e = find_child(dialog, QCheckBox, "uso_e")
    uso_e_1 = find_child(dialog, QLineEdit, "uso_e_1")
    uso_f = find_child(dialog, QCheckBox, "uso_f")
    uso_f_1 = find_child(dialog, QLineEdit, "uso_f_1")
    uso_g = find_child(dialog, QCheckBox, "uso_g")
    uso_g_1 = find_child(dialog, QLineEdit, "uso_g_1")
    occupanti = find_child(dialog, QLineEdit, "occupanti")
    localita = find_child(dialog, QComboBox, "localita")
    cod_local = find_child(dialog, QLineEdit, "cod_local")
    pr_pubb = find_child(dialog, QCheckBox, "pr_pubb")
    pr_priv = find_child(dialog, QCheckBox, "pr_priv")
    indirizzo = find_child(dialog, QLineEdit, "indirizzo")
    fronte = find_child(dialog, QComboBox, "fronte")
    n_interr = find_child(dialog, QComboBox, "n_interr")
    alt_piano = find_child(dialog, QComboBox, "alt_piano")
    vol_unico = find_child(dialog, QComboBox, "vol_unico")
    cord_cat = find_child(dialog, QComboBox, "cord_cat")
    pilastri = find_child(dialog, QComboBox, "pilastri")
    pilotis = find_child(dialog, QComboBox, "pilotis")
    sopraelev = find_child(dialog, QComboBox, "sopraelev")
    danno = find_child(dialog, QComboBox, "danno")
    stato_man = find_child(dialog, QComboBox, "stato_man")
    morf = find_child(dialog, QComboBox, "morf")

    alert_as = find_child(dialog, QLabel, "text_alert_as")
    alert_us = find_child(dialog, QLabel, "text_alert_us")
    alert_ae = find_child(dialog, QLabel, "text_alert_ae")
    alert_ac = find_child(dialog, QLabel, "text_alert_ac")

    alert_as.hide()
    alert_us.hide()
    alert_ae.hide()
    alert_ac.hide()
    inst_name.hide()
    inst_fran.hide()
    inst_liq.hide()
    inst_fag.hide()
    inst_ced.hide()
    inst_cav.hide()

    posizio.setEnabled(False)
    specialis.setEnabled(False)
    tipo_mur.setEnabled(False)
    uso_a.setEnabled(False)
    uso_a_1.setEnabled(False)
    uso_b.setEnabled(False)
    uso_b_1.setEnabled(False)
    uso_c.setEnabled(False)
    uso_c_1.setEnabled(False)
    uso_d.setEnabled(False)
    uso_d_1.setEnabled(False)
    uso_e.setEnabled(False)
    uso_e_1.setEnabled(False)
    uso_f.setEnabled(False)
    uso_f_1.setEnabled(False)
    uso_g.setEnabled(False)
    uso_g_1.setEnabled(False)

    help_button = find_child(dialog, QPushButton, "help_button")
    help_button.clicked.connect(partial(webbrowser.open,
                                        'https://www.youtube.com/watch?v=drs3COLtML8'))
    help_button.setEnabled(False)  # to delete

    button_box = find_child(dialog, QDialogButtonBox, "button_box")

    validation_callback = partial(form_validator, button_box, dialog)

    def _init():
        """Connect validator"""

        try:

            localita.currentIndexChanged.connect(
                validation_callback)
            ID_aggr.editingFinished.connect(validation_callback)
            ID_unit.editingFinished.connect(validation_callback)
            indirizzo.textEdited.connect(validation_callback)
            civico.textEdited.connect(validation_callback)
            occupanti.textEdited.connect(validation_callback)
            isolato.currentIndexChanged.connect(
                validation_callback)
            fronte.currentIndexChanged.connect(
                validation_callback)
            spec.currentIndexChanged.connect(validation_callback)
            n_interr.currentIndexChanged.connect(
                validation_callback)
            n_piani.textEdited.connect(validation_callback)
            alt_totale.textEdited.connect(validation_callback)
            alt_piano.currentIndexChanged.connect(
                validation_callback)
            vol_unico.currentIndexChanged.connect(
                validation_callback)
            superf_m.textEdited.connect(validation_callback)
            strutt_ver.currentIndexChanged.connect(
                validation_callback)
            cord_cat.currentIndexChanged.connect(
                validation_callback)
            pilastri.currentIndexChanged.connect(
                validation_callback)
            pilotis.currentIndexChanged.connect(
                validation_callback)
            sopraelev.currentIndexChanged.connect(
                validation_callback)
            danno.currentIndexChanged.connect(
                validation_callback)
            stato_man.currentIndexChanged.connect(
                validation_callback)
            morf.currentIndexChanged.connect(validation_callback)

            zona_ms.currentIndexChanged.connect(validation_callback)
            for field_name in ('inst_fran', 'inst_liq', 'inst_fag', 'inst_ced', 'inst_cav'):
                dialog.findChild(QCheckBox, field_name).stateChanged.connect(
                    validation_callback)

            ID_area.textEdited.connect(validation_callback)
            ID_infra_a.textEdited.connect(validation_callback)
            ID_infra_b.textEdited.connect(validation_callback)
            ID_infra_c.textEdited.connect(validation_callback)
            ID_infra_d.textEdited.connect(validation_callback)
            pr_pubb.stateChanged.connect(validation_callback)
            pr_priv.stateChanged.connect(validation_callback)

            # Connect usi and epoca
            usi = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
            for uso in usi:
                find_child(dialog, QCheckBox, 'uso_%s' %
                           uso).stateChanged.connect(validation_callback)
                find_child(dialog, QLineEdit, 'uso_%s_1' %
                           uso).textEdited.connect(validation_callback)

            for epoca in range(1, 9):
                dialog.findChild(QCheckBox, 'epoca_%s' %
                                 epoca).stateChanged.connect(validation_callback)

            validation_callback()

        except Exception as ex:
            QgsMessageLog.logMessage(
                'Exception in init: %s' % ex, 'CLETools', Qgis.Info)
            pass

    localita.currentIndexChanged.connect(
        partial(update_localita, dialog, cod_local, localita))
    sezione.textEdited.connect(partial(update_valore, sezione))
    ID_aggr.editingFinished.connect(
        partial(zero_digit, ID_aggr, alert_as, 10, 1))
    ID_unit.editingFinished.connect(
        partial(zero_digit, ID_unit, alert_us, 3, 0))
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
    civico.textEdited.connect(partial(update_valore, civico))
    n_piani.textEdited.connect(partial(update_valore, n_piani))
    alt_totale.textEdited.connect(partial(update_valore, alt_totale))
    superf_m.textEdited.connect(partial(update_valore, superf_m))
    isolato.currentIndexChanged.connect(
        partial(disablePosizio, dialog))
    spec.currentIndexChanged.connect(partial(disableSpecialis, dialog))
    strutt_ver.currentIndexChanged.connect(
        partial(disableTipo_mur, dialog))
    occupanti.textEdited.connect(partial(update_valore, occupanti))
    uso_a.stateChanged.connect(partial(check_button_1, dialog))
    uso_b.stateChanged.connect(partial(check_button_2, dialog))
    uso_c.stateChanged.connect(partial(check_button_3, dialog))
    uso_d.stateChanged.connect(partial(check_button_4, dialog))
    uso_e.stateChanged.connect(partial(check_button_5, dialog))
    uso_f.stateChanged.connect(partial(check_button_6, dialog))
    uso_g.stateChanged.connect(partial(check_button_7, dialog))

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
    superf_m.setText(area)

    QTimer.singleShot(200, _init)


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


def field_int_val(dialog, field_name):
    """Returns int value or 0 of the given field_name"""

    try:
        return int(field_text(dialog, field_name))
    except:
        return 0


def form_validator(button_box, dialog):

    find_child(dialog, QLabel, 'error_text').setText('')
    find_child(dialog, QGroupBox, 'message_box').hide()
    for label in dialog.findChildren((QLabel, QCheckBox)):
        label.setStyleSheet('')

    # Map of field names -> field number
    REQUIRED_FIELDS = {
        'indirizzo': 10,
        'civico': 11,
        'isolato': 13,
        'fronte': 15,
        'spec': 16,

        'n_piani': 18,
        'n_interr': 19,
        'alt_piano': 20,
        'alt_totale': 21,
        'vol_unico': 22,
        'superf_m': 23,
        'strutt_ver': 24,

        'cord_cat': 26,
        'pilastri': 27,
        'pilotis': 28,
        'sopraelev': 29,
        'danno': 30,
        'stato_man': 31,

        'morf': 34,

        'alluvio': 47,
        'uso_att': 48,

        'utilizz': 51,
        'occupanti': 52,
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

    if len(field_text(dialog, 'ID_unit')) != 3:
        errors.add(
            'Campo 7: e\' obbligatorio e deve essere lungo esattamente 3 caratteri!')

    if field_text(dialog, 'ID_unit'):
        try:
            if int(field_text(dialog, 'ID_unit')) == 0:
                errors.add('Campo 7: deve essere maggiore di zero!')
        except:
            errors.add('Campo 7: deve essere un numero valido!')

    # one of 9 a-d
    is_set = False
    i = 0
    infra_fields = ('ID_infra_a', 'ID_infra_b', 'ID_infra_c', 'ID_infra_d')
    for field_name in infra_fields:
        field_index = '9%s' % ['a', 'b', 'c', 'd'][i]
        text = field_text(dialog, field_name)
        if text:
            is_set = True
            try:
                if int(text) == 0:
                    errors.add('Campo 9: deve essere maggiore di zero!')
                if len(text) > 10:
                    errors.add(
                        'Campo 9: deve essere lungo esattamente 10 caratteri!')
            except:
                errors.add('Campo 9: deve essere un numero valido!')
            break

        i += 1

    if not is_set and not field_text(dialog, 'ID_area'):
        errors.add(
            'Campo 9: deve contenere almeno un identificatore di struttura diverso da zero oppure il campo 8 deve essere compilato!')

    is_set_8 = field_text(dialog, 'ID_area') != ''
    if is_set_8:
        fronte = find_child(dialog, QComboBox, "fronte")
        fronte.setCurrentIndex(fronte.findText('Vero'))

    if field_text(dialog, 'isolato') == 'Falso' and field_text(dialog, 'posizio') == '':
        errors.add(
            'Campo 14: e\' obbigatorio perche\' il campo 13 e\' "Falso"!')

    if field_text(dialog, 'spec') == 'Vero' and field_text(dialog, 'specialis') == '':
        errors.add(
            'Campo 17: e\' obbigatorio perche\' il campo 16 e\' "Vero"!')

    if field_int_val(dialog, 'n_piani') <= 0:
        errors.add(
            'Campo 18: deve essere un numero valido maggiore di zero!')

    if field_int_val(dialog, 'alt_totale') <= 0:
        errors.add(
            'Campo 21: deve essere un numero valido maggiore di zero!')

    # tipo_mur (25) required if 24 == 4 or 5
    strutt_ver_text = field_text(dialog, 'strutt_ver')
    if not field_text(dialog, 'tipo_mur') and strutt_ver_text in ("4 - Muratura", "5 - Mista (muratura/c.a.)"):
        errors.add(
            'Campo 25: e\' obbligatorio perche\' il campo 24 e\' impostato a 4 (Muratura) o 5 (Mista)!')

    # 32 / 33
    if not find_child(dialog, QCheckBox, 'pr_priv').isChecked() and not find_child(dialog, QCheckBox, 'pr_pubb').isChecked():
        errors.add(
            'Campo 32: questo campo oppure il campo 33 devono essere compilati!')
        errors.add(
            'Campo 33: questo campo oppure il campo 32 devono essere compilati!')

    # 38-42 required if 37 == 3
    zona_ms_instabile = field_text(dialog, 'zona_ms') == "3 - Instabile"
    for field_name in ('inst_fran', 'inst_liq', 'inst_fag', 'inst_ced', 'inst_cav'):
        item = dialog.findChild(QCheckBox, field_name)
        item.setVisible(zona_ms_instabile)
        if not zona_ms_instabile:
            item.setChecked(False)

    if zona_ms_instabile:
        is_set = False
        for field_name in ('inst_fran', 'inst_liq', 'inst_fag', 'inst_ced', 'inst_cav'):
            if dialog.findChild(QCheckBox, field_name).isChecked():
                is_set = True
                break

        if not is_set:
            errors.add(
                'Campo 38-42: almeno un tipo di instabilita\' deve essere selezionato!')

    # one of 49 uso_%s + uso_%s_1
    is_set = False
    usi = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
    for uso in usi:
        if find_child(dialog, QCheckBox, 'uso_%s' % uso).isChecked():
            try:
                int(field_text(dialog, 'uso_%s_1' % uso))
                is_set = True
            except:
                errors.add(
                    'Campo 49: uso "%s" deve essere un valore numerico!' % uso)

    if not is_set:
        errors.add('Campo 49: compilare almeno un tipo di uso!')

    # 50: one of (and just one)
    is_set = 0
    for epoca in range(1, 9):
        if dialog.findChild(QCheckBox, 'epoca_%s' % epoca).isChecked():
            is_set += 1

    if is_set != 1:
        errors.add(
            'Campo 50: selezionare una singola epoca di costruzione/ristrutturazione!')

    not_zero = {
        'occupanti': 52,
    }
    for name, idx in not_zero.items():
        if field_int_val(dialog, name) <= 0:
            errors.add(
                f'Campo {idx}: deve essere un numero valido maggiore di zero!')

    # Standard routines
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
                set_label_error(dialog, field_index, error_message)

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


def check_button_1(dialog):
    uso_a = find_child(dialog, QCheckBox, "uso_a")
    uso_a_1 = find_child(dialog, QLineEdit, "uso_a_1")
    if uso_a.isChecked() == True:
        uso_a_1.setEnabled(True)
    else:
        uso_a_1.setText("")
        uso_a_1.setEnabled(False)


def check_button_2(dialog):
    uso_b = find_child(dialog, QCheckBox, "uso_b")
    uso_b_1 = find_child(dialog, QLineEdit, "uso_b_1")
    if uso_b.isChecked() == True:
        uso_b_1.setEnabled(True)
    else:
        uso_b_1.setText("")
        uso_b_1.setEnabled(False)


def check_button_3(dialog):
    uso_c = find_child(dialog, QCheckBox, "uso_c")
    uso_c_1 = find_child(dialog, QLineEdit, "uso_c_1")
    if uso_c.isChecked() == True:
        uso_c_1.setEnabled(True)
    else:
        uso_c_1.setText("")
        uso_c_1.setEnabled(False)


def check_button_4(dialog):
    uso_d = find_child(dialog, QCheckBox, "uso_d")
    uso_d_1 = find_child(dialog, QLineEdit, "uso_d_1")
    if uso_d.isChecked() == True:
        uso_d_1.setEnabled(True)
    else:
        uso_d_1.setText("")
        uso_d_1.setEnabled(False)


def check_button_5(dialog):
    uso_e = find_child(dialog, QCheckBox, "uso_e")
    uso_e_1 = find_child(dialog, QLineEdit, "uso_e_1")
    if uso_e.isChecked() == True:
        uso_e_1.setEnabled(True)
    else:
        uso_e_1.setText("")
        uso_e_1.setEnabled(False)


def check_button_6(dialog):
    uso_f = find_child(dialog, QCheckBox, "uso_f")
    uso_f_1 = find_child(dialog, QLineEdit, "uso_f_1")
    if uso_f.isChecked() == True:
        uso_f_1.setEnabled(True)
    else:
        uso_f_1.setText("")
        uso_f_1.setEnabled(False)


def check_button_7(dialog):
    uso_g = find_child(dialog, QCheckBox, "uso_g")
    uso_g_1 = find_child(dialog, QLineEdit, "uso_g_1")
    if uso_g.isChecked() == True:
        uso_g_1.setEnabled(True)
    else:
        uso_g_1.setText("")
        uso_g_1.setEnabled(False)


def disablePosizio(dialog):
    isolato = find_child(dialog, QComboBox, "isolato")
    posizio = find_child(dialog, QComboBox, "posizio")
    if isolato.currentText() == "Falso":
        posizio.setEnabled(True)
        try:
            posizio.removeItem(3)
        except:
            pass
    if isolato.currentText() == "Vero":
        posizio.addItem('')
        posizio.setCurrentIndex(3)
        posizio.setEnabled(False)


def disableSpecialis(dialog):
    spec = find_child(dialog, QComboBox, "spec")
    specialis = find_child(dialog, QComboBox, "specialis")
    if spec.currentText() == "Vero":
        specialis.setEnabled(True)
        try:
            specialis.removeItem(4)
        except:
            pass
    if spec.currentText() == "Falso":
        specialis.addItem('')
        specialis.setCurrentIndex(4)
        specialis.setEnabled(False)


def disableTipo_mur(dialog):
    strutt_ver = find_child(dialog, QComboBox, "strutt_ver")
    tipo_mur = find_child(dialog, QComboBox, "tipo_mur")
    if strutt_ver.currentText() in ("4 - Muratura", "5 - Mista (muratura/c.a.)"):
        tipo_mur.setEnabled(True)
        try:
            tipo_mur.removeItem(3)
        except:
            pass
    else:
        tipo_mur.addItem('')
        tipo_mur.setCurrentIndex(3)
        tipo_mur.setEnabled(False)


def update_localita(dialog, cod_local, localita):
    localita = find_child(dialog, QComboBox, "localita")
    cod_local = find_child(dialog, QLineEdit, "cod_local")
    try:
        TipoIndagine = str(localita.currentText().strip()).split("  -  ")[1]
        cod_local.setText(TipoIndagine)
    except:
        pass
