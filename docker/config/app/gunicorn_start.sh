#!/bin/bash

logLevel="debug"
name="app"
frameworkFolder="/var/www/app/src/djangoprj"
sockfile=/var/run/gunicorn/app_gunicorn.sock
#django_settings_module=djangoprj.settings
django_wsgi=djangoprj.wsgi

user=www-data
group=www-data
num_workers=$(( 2 * `cat /proc/cpuinfo | grep 'core id' | wc -l` + 1 ))
timeout=600
#pythonenv="/var/www/app/src/pythonenv"

cd ${frameworkFolder}
#source ${pythonenv}/bin/activate
##export django_settings_module=${django_settings_module}
export PYTHONPATH=${frameworkFolder}:${PYTHONPATH}
rundir=$(dirname ${sockfile})
test -d ${rundir} || mkdir -p ${rundir}

#exec ${pythonenv}/bin/gunicorn ${django_wsgi}:application \
exec /usr/local/bin/gunicorn ${django_wsgi}:application \
  --name ${name} \
  --workers ${num_workers} \
  --timeout ${timeout} \
  --user=${user} --group=${group} \
  --bind 0.0.0.0:8000 \
  --log-level=${logLevel} \
  --access-logfile=/var/log/gunicorn/access.log \
  --error-logfile=/var/log/gunicorn/error.log
