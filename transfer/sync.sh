#!/usr/bin/env bash

if [[ -z ${INFOPANKKI_SYNC_SCRIPT} ]]; 
then 
	echo "Transfer infopankki data"
	lftp -f ${INFOPANKKI_SYNC_SCRIPT}
else
	echo "No sync script, exiting"
	exit 1
fi

rc=$?;
if [[ ${rc} != 0 ]]; then exit ${rc}; fi

echo "Import started"
$HOME/info/venv/bin/python manage.py import

rc=$?;
if [[ ${rc} != 0 ]]; then exit ${rc}; fi


if [[ -z ${INFOPANKKI_IMPORT_HEALTH_CHECK} ]]; 
then 
	echo "Calling health check"
	curl --retry 3 $INFOPANKKI_IMPORT_HEALTH_CHECK
fi

rc=$?;
if [[ ${rc} != 0 ]]; then exit ${rc}; fi
