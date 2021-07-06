Introduzione
============

Analisi della condizione limite per l'emergenza dell'insediamento urbano
------------------------------------------------------------------------

Dopo il terremoto in Abruzzo del 6 aprile 2009, è stato lanciato il *"Piano nazionale per la prevenzione del rischio sismico"* (legge 77/2009 art. 11) e sono state assegnate risorse sulla base dell’indice medio di rischio sismico dei territori per la realizzazione degli studi di microzonazione sismica. 

Per la realizzazione di tali studi, il documento tecnico di riferimento è rappresentato dal **"Manuale per l’analisi della Condizione Limite per l’Emergenza (CLE) dell’insediamento urbano"** (*Commissione tecnica per la microzonazione sismica, 2014*), di seguito **MCLE 2014**. 

Per supportare gli architetti e per facilitare e omogeneizzare l’elaborazione delle carte per l’analisi della Condizione Limite per l’Emergenza (CLE), sono stati predisposti gli **"Standard di rappresentazione ed archiviazione informatica**", 2018 (di seguito Standard CLE). Questo documento costituisce il riferimento per la creazione di prodotti cartografici e per l’archiviazione delle informazioni utili per lo svolgimento degli studi.

Secondo gli *MCLE 2014* e gli *Standard CLE*, il prodotto cartografico da presentare negli studi di MS è la carta per l’analisi della Condizione Limite per l’Emergenza. Attualmente gli Standard CLE prevedono la creazione di un archivio digitale basato su shapefile e tabelle in formato *.mdb* (database Microsoft Access), organizzati secondo una struttura ben definita.

Il plugin **CLE Tools** è stato realizzato con l'obiettivo di semplificare la creazione del database e del prodotto cartografico per la CLE, sfruttando le potenzialità dei software liberi `QGIS <https://qgis.org>`_ ed `SQLite/SpatiaLite <https://www.gaia-gis.it/fossil/libspatialite/index>`_, e del linguaggio di programmazione Python.

Il plugin **CLE Tools** è pubblicato tramite il `repository ufficiale <https://plugins.qgis.org/plugins/CLETools/>`_ dei plugin di QGIS ed è scaricabile direttamente tramite l’interfaccia di gestione delle estensioni di QGIS. Inoltre lo sviluppo del Plugin è aperto e i contributi, sotto forma di codice, suggerimenti e segnalazioni, possono essere proposti da chiunque tramite la piattaforma `GitHub <https://github.com/CNR-IGAG/cle-tools>`_. 

Credits
-------

|logo_igag| |logo_cnr|

.. |logo_igag| image:: ./img/IGAG-CMYK.png
    :width: 18%
    :target: https://www.igag.cnr.it

.. |logo_cnr| image:: ./img/logo_cnr.png
    :width: 30%

Il plugin viene sviluppato nell'ambito delle attività del 
`Laboratorio GIS del CNR-IGAG <https://www.igag.cnr.it/lista-laboratori/labgis/>`_

Riferimenti
-----------

* Commissione tecnica per la microzonazione sismica. *Manuale per l’analisi della Condizione Limite per l’Emergenza (CLE) dell’insediamento urbano.* Roma: Presidenza del Consiglio dei Ministri - Dipartimento della protezione civile. Tratto, il giorno 18 agosto del 2018, dal sito del `CentroMS <https://www.centromicrozonazionesismica.it/it/download/send/33-manuale-per-l-analisi-della-condizione-lite-per-l-emergenza-cle-dell-insediamento-urbano/89-manuale-per-l-analisi-della-condizione-lite-per-l-emergenza-cle-dell-insediamento-urbano>`_
* Commissione tecnica per la microzonazione sismica. *Standard di rappresentazione e archiviazione informatica – Analisi della condizione limite per l’emergenza (CLE) (versione 3.1).* Roma: Commissione tecnica per la microzonazione sismica. Tratto, il giorno 20 dicembre del 2019, dal sito del `CentroMS <https://www.centromicrozonazionesismica.it/it/download/send/25-standardcle-31/70-standardclev3-1>`_
* Manuale utente di QGIS 3.16  tratto il giorno 10/06/2021 da https://docs.qgis.org/3.16/it/docs/user_manual/ 
