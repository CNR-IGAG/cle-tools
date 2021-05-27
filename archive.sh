#!/bin/bash
# Crea il pacchetto zip dal branch specificato in riga di comando (default: master) 

BRANCH=${1:-master}

git archive --prefix cle-tools/ --format=zip -o cle-tool-qgis3.zip ${BRANCH}


