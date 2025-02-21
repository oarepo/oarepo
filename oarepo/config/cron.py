from datetime import timedelta
from typing import Any

from celery.schedules import crontab
from invenio_stats.tasks import StatsAggregationTask, StatsEventTask

from .base import set_constants_in_caller


def configure_cron(**extra_cron_items: Any) -> None:
    CELERY_BEAT_SCHEDULE = {
        "indexer": {
            "task": "invenio_records_resources.tasks.manage_indexer_queues",
            "schedule": timedelta(seconds=10),
        },
        "accounts_sessions": {
            "task": "invenio_accounts.tasks.clean_session_table",
            "schedule": timedelta(minutes=60),
        },
        "accounts_ips": {
            "task": "invenio_accounts.tasks.delete_ips",
            "schedule": timedelta(hours=6),
        },
        # "draft_resources": {
        #     "task": ("invenio_drafts_resources.services.records.tasks.cleanup_drafts"),
        #     "schedule": timedelta(minutes=60),
        # },
        # "rdm_records": {
        #     "task": "invenio_rdm_records.services.tasks.update_expired_embargos",
        #     "schedule": crontab(minute=2, hour=0),
        # },
        # "expire_requests": {
        #     "task": "invenio_requests.tasks.check_expired_requests",
        #     "schedule": crontab(minute=3, hour=0),
        # },
        # "file-checks": {
        #     "task": "invenio_files_rest.tasks.schedule_checksum_verification",
        #     "schedule": timedelta(hours=1),
        #     "kwargs": {
        #         "batch_interval": {"hours": 1},
        #         "frequency": {"days": 14},
        #         "max_count": 0,
        #         # Query taking into account only files with URI prefixes defined by
        #         # the FILES_REST_CHECKSUM_VERIFICATION_URI_PREFIXES config variable
        #         "files_query": "invenio_app_rdm.utils.files.checksum_verification_files_query",
        #     },
        # },
        # "file-integrity-report": {
        #     "task": "invenio_app_rdm.tasks.file_integrity_report",
        #     "schedule": crontab(minute=0, hour=7),  # Every day at 07:00 UTC
        # },
        # indexing of statistics events & aggregations
        "stats-process-events": {
            **StatsEventTask,
            "schedule": crontab(minute="25,55"),  # Every hour at minute 25 and 55
        },
        "stats-aggregate-events": {
            **StatsAggregationTask,
            "schedule": crontab(minute=0),  # Every hour at minute 0
        },
        # "reindex-stats": StatsRDMReindexTask,  # Every hour at minute 10
        # Invenio communities provides some caching that has the potential to be never removed,
        # therefore, we need a cronjob to ensure that at least once per day we clear the cache
        "clear-cache": {
            "task": "invenio_communities.tasks.clear_cache",
            "schedule": crontab(minute=0, hour=1),  # Every day at 01:00 UTC
        },
        "clean-access-request-tokens": {
            "task": "invenio_rdm_records.requests.access.tasks.clean_expired_request_access_tokens",
            "schedule": crontab(minute=4, hour=0),
        },
        **extra_cron_items,
    }

    set_constants_in_caller(locals())
