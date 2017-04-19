#!/usr/bin/env bash

export INFOPANKKI_TRANSFER_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $INFOPANKKI_TRANSFER_ROOT/..

echo "Transfer infopankki data"
lftp -f ${INFOPANKKI_TRANSFER_ROOT}/lftp_sync

rc=$?;
if [[ ${rc} != 0 ]]; then exit ${rc}; fi

echo "Import startup"
env $(cat .env | grep -v "^#" | xargs) $HOME/info/venv/bin/python manage.py import

rc=$?;
if [[ ${rc} != 0 ]]; then exit ${rc}; fi

echo "Calling health check"
curl --retry 3 https://hchk.io/c993b23c-ddc3-49b9-8169-7407d630d7f7

rc=$?;
if [[ ${rc} != 0 ]]; then exit ${rc}; fi
