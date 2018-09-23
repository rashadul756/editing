import json
from datetime import datetime

from django.db import models
from django.conf import settings


class TimeStampModel(models.Model):
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_modified_date(self):
        return self.modified_date.strftime('%b %d, %Y')


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)