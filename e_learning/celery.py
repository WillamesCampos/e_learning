import os
from celery import Celery

# Configurar o Django para que o Celery possa descobrir as configurações do projeto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_learning.settings')

app = Celery('e_learning')

# Configurar o Celery usando as configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobrir e registrar as tarefas do Celery no Django
app.autodiscover_tasks()
