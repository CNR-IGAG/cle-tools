.. _editing:

Inserimento dati ed editing
---------------------------

.. |ico4| image:: ../../../img/ico_edita.png
  :height: 25

.. |ico5| image:: ../../../img/ico_salva_edita.png
  :height: 25

Il plugin possiede alcuni strumenti che aiutano l’operatore nel disegno e nella creazione di nuovi oggetti secondo determinate regole topologiche preimpostate nel progetto.

La procedura per **inserire nuovi dati** consiste in:

* selezionare il layer da editare nel pannello dei layer di QGIS;
* attivare l’editing con lo strumento |ico4| della toolbar del plugin;
* disegnare su mappa la geometria dell’elemento;
* una volta conclusa la digitalizzazione (tramite il pulsante destro del mouse), QGIS aprirà automaticamente la maschera di inserimento degli attributi relativi alla geometria appena creata;
* dopo aver inserito gli attributi, premere il tasto “OK” della maschera di inserimento;
* per salvare, cliccare il tool del plugin “Save” |ico5|.

.. note:: È possibile attivare l’editing anche tramite le funzionalità native di QGIS, ma il pulsante |ico4| della toolbar di MzSTools consente di impostare automaticamente, per determinati layer, una configurazione di *snapping* che consente di evitare **errori topologici** quali intersezioni ed auto-intersezioni fra geometrie, anche di layer diversi, come indicato negli Standard MS.

Per **modificare gli attributi** di una feature già esistente, è possibile procedere in questo modo:

* selezionare il layer da editare;
  
  .. image:: ../img/editing1.png
      :width: 350
      :align: center

* attivare l’editing con:

  - lo strumento della toolbar di QGIS “Attiva modifiche”;
  - oppure lo strumento |ico4| della barra del plugin;

* "identificare" la feature da editare su mappa tramite lo strumento "Informazioni elementi" di QGIS;
  
  .. tip:: Per fare in modo che QGIS apra direttamente la maschera di inserimento, nel pannello “Informazioni risultati” mettere la spunta su “Apri modulo automaticamente”.
  
    .. image:: ../img/ident_maschera.png
        :width: 550
        :align: center

* all’interno della maschera, modificare i campi da aggiornare. La finestra di inserimento può essere più o meno articolata in base alla quantità di informazioni correlate alla geometria inserita;

  .. image:: ../img/editing2.png
      :width: 700
      :align: center

* per salvare le modifiche, cliccare su:

  * pulsante della toolbar di QGIS “Salva modifiche vettore”;
  * oppure pulsante della barra del plugin |ico5|.
