import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def test_task():
    print('Celery is working.')
    logger.info('Celery is working.')
