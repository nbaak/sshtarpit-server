#!/bin/sh

THIS_DIR=$(dirname $(readlink -f $0))

# move secret to auth.token
echo "# env file" > ${THIS_DIR}/.env
echo COUNTIT_AUTH_TOKEN=$AUTH_TOKEN >> ${THIS_DIR}/.env
echo $AUTH_TOKEN > ${THIS_DIR}/countit.token
echo COUNTIT_SERVER=$COUNTIT_SERVER >> ${THIS_DIR}/.env
echo COUNTIT_PORT=$COUNTIT_PORT >> ${THIS_DIR}/.env

echo GEOIP_SERVER=$GEOIP_SERVER >> ${THIS_DIR}/.env

python /tarpit/app.py
# gunicorn -w 1 -b "0.0.0.0:22222" "app:app"
