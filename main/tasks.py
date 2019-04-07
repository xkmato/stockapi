import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def collect_price_updates():
    logger.info(
        "Supposed to periodically collect price update info from external resource"
    )
