from __future__ import unicode_literals
from django.contrib.auth.models import User

from committee.models import Committee

from django.db import models

class Item(models.Model):
    NEW = 'N'
    PREAPPROVED = 'C'
    PROCESSED = 'P'
    REJECTED = 'R'

    STATUS = (
        (NEW, 'New'),
        (PREAPPROVED, 'Committee Approved'),
        (PROCESSED, 'Processed'),
        (REJECTED, 'Rejected'),
    )

    desc = models.CharField(max_length=200)
    event = models.CharField(max_length=200)
    committee = models.ForeignKey(Committee)
    details = models.TextField()
    cost = models.DecimalField(max_digits=7, decimal_places=2)
    date_purchased = models.DateField('date purchased')

    created_by = models.ForeignKey(User, related_name='created_by')
    approved_by = models.ManyToManyField(User, blank=True, related_name='approved_by')
    date_filed = models.DateTimeField('date filed')
    status = models.CharField(max_length=2, choices=STATUS)
    task_id = models.CharField(max_length=30)

    def approved(self):
        return self.status == 'P'

    def processed(self):
        return self.status == 'C'

    def rejected(self):
        return self.status == 'R'

    def new(self):
        return self.status == 'N'

    def comName(self):
        return self.committee.name

    def __str__(self):
        return self.committee.name + ": " + self.event + " " + self.desc

    @staticmethod
    def parseDate(date_str):
        try:
            return datetime.strptime(date_str, "%m/%d/%y").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%m/%d/%Y").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%m-%d-%y").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%m-%d-%Y").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%m %d %y").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%m %d %Y").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%y %m %d").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%Y %m %d").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%y-%m-%d").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%y/%m/%d").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%Y/%m/%d").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%d %m %y").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%d %m %Y").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%d/%m/%y").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%d-%m-%y").date().isoformat()
        except ValueError:
            pass
        try:
            return datetime.strptime(date_str, "%d-%m-%Y").date().isoformat()
        except ValueError:
            return date.today().isoformat()
