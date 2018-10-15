import os
import django
from celery import Celery
from django.core.mail import send_mail

'''分布式任务队列'''

app = Celery('celery_tasks.tasks', broker='redis://192.168.12.193:6379/2')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyItem.settings")
django.setup()


@app.task
def task_send_mail(subject, message, sender, receiver, html_message):
    send_mail(subject, message, sender, receiver, html_message=html_message)
