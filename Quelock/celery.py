from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quelock.settings')

app = Celery('Quelock')

# Using a string here means the worker will not have to
# pickle the object when using Windows.


app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.broker_transport_options = {'fanout_prefix': True}
app.conf.broker_transport_options = {'visibility_timeout': 43200}
app.conf.result_backend = 'redis://localhost:6379/1/'
