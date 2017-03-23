#!/usr/bin/env bash

export INFOPANKKI_ROOT = $HOME/infopankki/

cd ${INFOPANKKI_ROOT}/api

lftp -f ${INFOPANKKI_ROOT}/infopankki_api/transfer/lftp_sync

$HOME/info/venv/python ${INFOPANKKI_ROOT}/manage.py

curl --retry 3 https://hchk.io/c993b23c-ddc3-49b9-8169-7407d630d7f7

