from celery import Celery
import os

app = Celery('project', 
        broker='redis://{}:6379/0'.format(os.getenv('REDIS_HOST')), 
        backend='redis://{}:6379/0'.format(os.getenv('REDIS_HOST')), 
        include=['project.tasks'])

if __name__=='__main__':
    app.start()
