import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'provet.settings')

app = Celery('provet')

# Read config from Django settings using namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
