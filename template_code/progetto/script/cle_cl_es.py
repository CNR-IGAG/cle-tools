# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:		cle_cl_es.py
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


def cl_es(dialog, layer, feature):
    #data_es = dialog.findChild(QgsDateTimeEdit,"data_es")
    #today = QDate.currentDate()
    # data_es.setDate(today)
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
    anno_prog = find_child(dialog, QLineEdit, "anno_prog")
    anno_cost = find_child(dialog, QLineEdit, "anno_cost")
    esp_pers = find_child(dialog, QLineEdit, "esp_pers")
    interv = find_child(dialog, QComboBox, "interv")
    interv_ann = find_child(dialog, QLineEdit, "interv_ann")
    interv_name = find_child(dialog, QLabel, "interv_name")
    interv_1 = find_child(dialog, QCheckBox, "interv_1")
    interv_2 = find_child(dialog, QCheckBox, "interv_2")
    interv_3 = find_child(dialog, QCheckBox, "interv_3")
    interv_4 = find_child(dialog, QCheckBox, "interv_4")
    interv_5 = find_child(dialog, QCheckBox, "interv_5")
    interv_6 = find_child(dialog, QCheckBox, "interv_6")
    interv_7 = find_child(dialog, QCheckBox, "interv_7")
    isolato = find_child(dialog, QComboBox, "isolato")
    posizio = find_child(dialog, QComboBox, "posizio")
    spec = find_child(dialog, QComboBox, "spec")
    specialis = find_child(dialog, QComboBox, "specialis")
    strutt_ver = find_child(dialog, QComboBox, "strutt_ver")
    tipo_mur = find_child(dialog, QComboBox, "tipo_mur")
    evento_1 = find_child(dialog, QComboBox, "evento_1")
    data_ev_1 = find_child(dialog, QWidget, "data_ev_1")
    tipo_1 = find_child(dialog, QComboBox, "tipo_1")
    date_label_1 = find_child(dialog, QLabel, "date_label_1")
    evento_2 = find_child(dialog, QComboBox, "evento_2")
    data_ev_2 = find_child(dialog, QWidget, "data_ev_2")
    tipo_2 = find_child(dialog, QComboBox, "tipo_2")
    date_label_2 = find_child(dialog, QLabel, "date_label_2")
    evento_3 = find_child(dialog, QComboBox, "evento_3")
    data_ev_3 = find_child(dialog, QWidget, "data_ev_3")
    tipo_3 = find_child(dialog, QComboBox, "tipo_3")
    date_label_3 = find_child(dialog, QLabel, "date_label_3")
    zona_ms = find_child(dialog, QComboBox, "zona_ms")
    inst_name = find_child(dialog, QLabel, "inst_name")
    inst_fran = find_child(dialog, QCheckBox, "inst_fran")
    inst_liq = find_child(dialog, QCheckBox, "inst_liq")
    inst_fag = find_child(dialog, QCheckBox, "inst_fag")
    inst_ced = find_child(dialog, QCheckBox, "inst_ced")
    inst_cav = find_child(dialog, QCheckBox, "inst_cav")
    localita = find_child(dialog, QComboBox, "localita")
    cod_local = find_child(dialog, QLineEdit, "cod_local")
    alert_as = find_child(dialog, QLabel, "text_alert_as")
    alert_us = find_child(dialog, QLabel, "text_alert_us")
    alert_ae = find_child(dialog, QLabel, "text_alert_ae")
    alert_ac = find_child(dialog, QLabel, "text_alert_ac")
    indirizzo = find_child(dialog, QLineEdit, "indirizzo")
    denom = find_child(dialog, QLineEdit, "denom")
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
    alluvio = find_child(dialog, QComboBox, "alluvio")
    uso_orig = find_child(dialog, QComboBox, "uso_orig")
    uso_att = find_child(dialog, QComboBox, "uso_att")
    ID_edif = find_child(dialog, QComboBox, "ID_edif")
    esp_ore = find_child(dialog, QComboBox, "esp_ore")
    esp_mes = find_child(dialog, QComboBox, "esp_mes")
    pr_pubb = find_child(dialog, QCheckBox, "pr_pubb")
    pr_priv = find_child(dialog, QCheckBox, "pr_priv")

    alert_as.hide()
    alert_us.hide()
    alert_ae.hide()
    alert_ac.hide()
    posizio.setEnabled(False)
    specialis.setEnabled(False)
    tipo_mur.setEnabled(False)
    inst_name.hide()
    inst_fran.hide()
    inst_liq.hide()
    inst_fag.hide()
    inst_ced.hide()
    inst_cav.hide()
    interv_ann.setEnabled(False)
    interv_name.hide()
    interv_1.hide()
    interv_2.hide()
    interv_3.hide()
    interv_4.hide()
    interv_5.hide()
    interv_6.hide()
    interv_7.hide()
    data_ev_1.hide()
    tipo_1.setEnabled(False)
    date_label_1.hide()
    data_ev_2.hide()
    tipo_2.setEnabled(False)
    date_label_2.hide()
    data_ev_3.hide()
    tipo_3.setEnabled(False)
    date_label_3.hide()

    help_button = find_child(dialog, QPushButton, "help_button")
    help_button.clicked.connect(partial(webbrowser.open,
                                        'https://www.youtube.com/watch?v=drs3COLtML8'))
    help_button.setEnabled(False)  # to delete

    button_box = find_child(dialog, QDialogButtonBox, "button_box")

    validation_callback = partial(validateForm, button_box, dialog)

    def _init():
        """Connect validator"""

        try:

            localita.currentIndexChanged.connect(
                validation_callback)
            ID_aggr.editingFinished.connect(validation_callback)
            ID_unit.editingFinished.connect(validation_callback)
            indirizzo.editingFinished.connect(validation_callback)
            civico.textEdited.connect(validation_callback)
            denom.textEdited.connect(validation_callback)
            isolato.currentIndexChanged.connect(
                validation_callback)
            fronte.currentIndexChanged.connect(
                validation_callback)
            spec.currentIndexChanged.connect(
                validation_callback)
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
            morf.currentIndexChanged.connect(
                validation_callback)
            alluvio.currentIndexChanged.connect(
                validation_callback)
            uso_orig.currentIndexChanged.connect(
                validation_callback)
            uso_att.currentIndexChanged.connect(
                validation_callback)
            ID_edif.currentIndexChanged.connect(
                validation_callback)
            esp_pers.textEdited.connect(validation_callback)
            esp_ore.currentIndexChanged.connect(
                validation_callback)
            esp_mes.currentIndexChanged.connect(
                validation_callback)
            interv.currentIndexChanged.connect(
                validation_callback)
            interv_ann.textChanged.connect(validation_callback)
            ID_area.textEdited.connect(validation_callback)
            ID_infra_a.textEdited.connect(validation_callback)
            ID_infra_b.textEdited.connect(validation_callback)
            ID_infra_c.textEdited.connect(validation_callback)
            ID_infra_d.textEdited.connect(validation_callback)
            anno_prog.textEdited.connect(validation_callback)
            anno_cost.textEdited.connect(validation_callback)
            pr_pubb.stateChanged.connect(validation_callback)
            pr_priv.stateChanged.connect(validation_callback)
            zona_ms.currentIndexChanged.connect(validation_callback)
            for field_name in ('inst_fran', 'inst_liq', 'inst_fag', 'inst_ced', 'inst_cav'):
                dialog.findChild(QCheckBox, field_name).stateChanged.connect(
                    validation_callback)

            for i in range(1, 8):
                field_name = 'interv_%s' % i
                find_child(dialog, QCheckBox, field_name).stateChanged.connect(
                    validation_callback)

            for emerg in range(1, 7):
                dialog.findChild(QCheckBox, 'emerg_%s' %
                                 emerg).stateChanged.connect(validation_callback)

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
    anno_prog.textEdited.connect(partial(update_valore, anno_prog))
    anno_cost.textEdited.connect(partial(update_valore, anno_cost))
    esp_pers.textEdited.connect(partial(update_valore, esp_pers))
    interv_ann.textEdited.connect(partial(update_valore, interv_ann))
    isolato.currentIndexChanged.connect(partial(disablePosizio, dialog))
    spec.currentIndexChanged.connect(partial(disableSpecialis, dialog))
    strutt_ver.currentIndexChanged.connect(partial(disableTipo_mur, dialog))
    evento_1.currentIndexChanged.connect(validation_callback)
    evento_2.currentIndexChanged.connect(validation_callback)
    evento_3.currentIndexChanged.connect(validation_callback)
    interv.currentIndexChanged.connect(partial(disableInterv, dialog))

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


def validateForm(button_box, dialog):
    """Form validator"""

    find_child(dialog, QLabel, 'error_text').setText('')
    find_child(dialog, QGroupBox, 'message_box').hide()
    for label in dialog.findChildren((QLabel, QCheckBox)):
        label.setStyleSheet('')

    # Map of field names -> field number
    REQUIRED_FIELDS = {
        'indirizzo': 10,
        'civico': 11,
        'denom': '12b',
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
        'ID_edif': 48,

        'uso_orig': 50,
        'uso_att': 51,
        'esp_pers': 54,
        'esp_ore': 55,
        'esp_mes': 56,
        'interv': 57,
        'verif_sism': 75,
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

    if not is_set:
        errors.add(
            'Campo 9: deve contenere almeno un identificativo di infrastruttura diverso da zero!')

    if field_text(dialog, 'isolato') == 'Falso' and field_text(dialog, 'posizio') == '':
        errors.add(
            'Campo 14: e\' obbigatorio perche\' il campo 13 e\' "Falso"!')

    if field_text(dialog, 'spec') == 'Vero' and field_text(dialog, 'specialis') == '':
        errors.add(
            'Campo 17: e\' obbigatorio perche\' il campo 16 e\' "Vero"!')

    # tipo_mur (25) required if 24 == 4 or 5
    strutt_ver_text = field_text(dialog, 'strutt_ver')
    if not field_text(dialog, 'tipo_mur') and strutt_ver_text in ("4 - Muratura", "5 - Mista (muratura/c.a.)"):
        errors.add(
            'Campo 25: e\' obbligatorio perche\' il campo 24 e\' impostato a 4 (Muratura) o 5 (Mista)!')

    is_set_8 = field_text(dialog, 'ID_area') != ''
    if is_set_8:
        fronte = find_child(dialog, QComboBox, "fronte")
        fronte.setCurrentIndex(fronte.findText('Vero'))

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

    if field_int_val(dialog, 'n_piani') <= 0:
        errors.add(
            'Campo 18: deve essere un numero valido maggiore di zero!')

    if field_int_val(dialog, 'alt_totale') <= 0:
        errors.add(
            'Campo 21: deve essere un numero valido maggiore di zero!')

    not_zero = {
        'esp_pers': 54,
        'esp_ore': 55,
        'esp_mes': 56,
    }
    for name, idx in not_zero.items():
        if field_int_val(dialog, name) <= 0:
            errors.add(
                f'Campo {idx}: deve essere un numero valido maggiore di zero!')

    # one of 52 53
    if field_int_val(dialog, 'anno_prog') <= 0 and field_int_val(dialog, 'anno_cost') <= 0:
        errors.add(
            'Campo 52: questo campo oppure il campo 53 devono essere compilati e maggiori di zero!')
        errors.add(
            'Campo 53: questo campo oppure il campo 52 devono essere compilati e maggiori di zero!')

    anno_prog = field_int_val(dialog, 'anno_prog')  # 52
    anno_cost = field_int_val(dialog, 'anno_cost')  # 53
    if anno_prog > 0 and anno_cost > 0 and anno_prog > anno_cost:
        errors.add(
            'Campo 52: non puo\' essere maggiore del campo 53!')
        errors.add(
            'Campo 53: non puo\' essere minore del campo 52!')

    edif_is_001 = field_text(dialog, 'ID_edif').startswith('001 ')

    for i in range(1, 7):
        field_name = 'emerg_%s' % i
        find_child(dialog, QCheckBox, field_name).setEnabled(edif_is_001)

    if edif_is_001:
        # 49: one of emerg_[1-6]
        is_set_49 = False
        for i in range(1, 7):
            field_name = 'emerg_%s' % i
            if find_child(dialog, QCheckBox, field_name).isChecked():
                is_set_49 = True
                break

        if not is_set_49:
            errors.add(
                'Campo 49: almeno un tipo di struttura deve essere selezionato!')

    # 54 esp_pers check int (0 is allowed)
    try:
        int(field_text(dialog, 'esp_pers'))
    except:
        errors.add('Campo 54: deve essere un numero valido!')

    if field_text(dialog, 'interv') == 'Vero':
        if not field_text(dialog, 'interv_ann'):
            errors.add(
                'Campo 58: e\' obbigatorio perche\' il campo 57 e\' "Vero"!')
        # Check one of 59-65
        is_set = False
        for i in range(1, 8):
            field_name = 'interv_%s' % i
            if find_child(dialog, QCheckBox, field_name).isChecked():
                is_set = True
                break
        if not is_set:
            errors.add(
                'Campo 59-65: almeno un tipo di intervento deve essere selezionato!')

    for evt in range(1, 4):
        enabled = find_child(dialog, QComboBox, 'evento_%s' %
                             evt).currentIndex() > 0
        date = find_child(dialog, QgsDateTimeEdit, 'data_ev_%s' % evt)
        date.setEnabled(enabled)
        tipo = find_child(dialog, QgsDateTimeEdit, 'tipo_%s' % evt)
        tipo.setEnabled(enabled)
        if enabled:
            date.show()
            tipo.show()

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


def alert_data(dialog):
    anno_prog = find_child(dialog, QLineEdit, "anno_prog")
    anno_cost = find_child(dialog, QLineEdit, "anno_cost")
    if (anno_prog.text() == '') and (anno_cost.text() == ''):
        pass
    elif (anno_prog.text() != '') and (anno_cost.text() != ''):
        if int(anno_prog.text()) > int(anno_cost.text()):
            QMessageBox.warning(
                None, 'WARNING!', "The value of the 'ANNO DI PROGETTAZIONE' field is greater than the value of the 'ANNO DI FINE COSTRUZIONE' field!")
            anno_prog.setText('')
            anno_cost.setText('')


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


def disableInterv(dialog):
    interv = find_child(dialog, QComboBox, "interv")
    interv_ann = find_child(dialog, QLineEdit, "interv_ann")
    interv_name = find_child(dialog, QLabel, "interv_name")
    interv_1 = find_child(dialog, QCheckBox, "interv_1")
    interv_2 = find_child(dialog, QCheckBox, "interv_2")
    interv_3 = find_child(dialog, QCheckBox, "interv_3")
    interv_4 = find_child(dialog, QCheckBox, "interv_4")
    interv_5 = find_child(dialog, QCheckBox, "interv_5")
    interv_6 = find_child(dialog, QCheckBox, "interv_6")
    interv_7 = find_child(dialog, QCheckBox, "interv_7")
    if interv.currentText() == "Vero":
        interv_name.show()
        interv_1.show()
        interv_2.show()
        interv_3.show()
        interv_4.show()
        interv_5.show()
        interv_6.show()
        interv_7.show()
        interv_ann.setEnabled(True)
        interv_1.setEnabled(True)
        interv_2.setEnabled(True)
        interv_3.setEnabled(True)
        interv_4.setEnabled(True)
        interv_5.setEnabled(True)
        interv_6.setEnabled(True)
        interv_7.setEnabled(True)
    else:
        interv_ann.setText("")
        interv_ann.setEnabled(False)
        interv_1.setChecked(False)
        interv_1.setEnabled(False)
        interv_2.setChecked(False)
        interv_2.setEnabled(False)
        interv_3.setChecked(False)
        interv_3.setEnabled(False)
        interv_4.setChecked(False)
        interv_4.setEnabled(False)
        interv_5.setChecked(False)
        interv_5.setEnabled(False)
        interv_6.setChecked(False)
        interv_6.setEnabled(False)
        interv_7.setChecked(False)
        interv_7.setEnabled(False)


def define_lista(cod_list, nome_tab):
    codici = QgsProject.instance().mapLayersByName(nome_tab)[0]

    for elem in codici.getFeatures(QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)):
        lista_cod = [elem.attributes()[0], elem.attributes()[1]]
        cod_list.append(lista_cod)
    return cod_list


def update_box(Qbox, cod_list):
    Qbox.clear()
    Qbox.addItem("")
    Qbox.model().item(0).setEnabled(False)
    for row in cod_list:
        Qbox.addItem(row[2])


def update_localita(dialog, cod_local, localita):
    localita = find_child(dialog, QComboBox, "localita")
    cod_local = find_child(dialog, QLineEdit, "cod_local")
    try:
        TipoIndagine = str(localita.currentText().strip()).split("  -  ")[1]
        cod_local.setText(TipoIndagine)
    except:
        pass
