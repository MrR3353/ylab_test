from celery import Celery

from config import RUN_ON_DOCKER

celery = None

if not RUN_ON_DOCKER:   # if running example without docker
    celery = Celery(
        'worker',
        backend='redis://localhost:6379',
        broker='amqp://localhost:5672'
    )
    # celery.conf.beat_schedule = {
    #     'task-name': {
    #         'task': 'tasks.update_db_from_admin',
    #         'schedule': 15.0
    #     },
    # }

else:   # running example with docker
    celery = Celery(
        'worker',
        backend='redis://redis:6379',
        broker='amqp://guest:guest@rabbitmq:5672'
    )

celery.conf.timezone = 'UTC'
