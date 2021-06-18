# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CLETools
                                 A QGIS plugin
 The plugin allows the creation of the database and the cartographic representation of the analysis of the Emergency Limit Condition according to the standards of representation and computer archiving version 3.1 (Technical Commission for seismic microzonation - art. 5, paragraph 7, OPCM 13 nov. 2010, n. 3907).
Il plugin consente la creazione della banca dati e la rappresentazione cartografica delle analisi della Condizione Limite per l'Emergenza secondo gli Standard di rappresentazione ed archiviazione informatica versione 3.1 (Commissione tecnica per la microzonazione sismica - art. 5, comma 7 dell’OPCM 13 nov. 2010, n. 3907).
                             -------------------
        begin                : 2019-01-15
        copyright            : (C) 2019 by IGAG-CNR
        email                : labgis@igag.cnr.it
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CLETools class from file CLETools.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .cle_tools import CLETools
    return CLETools(iface)
