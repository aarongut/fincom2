from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.mail import send_mail
from storages.backends.s3boto3 import S3Boto3Storage
from stdimage.models import StdImageField
from datetime import datetime, date

from committee.models import Committee

from django.db import models

class Item(models.Model):
    S3 = S3Boto3Storage()

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
    image = StdImageField(upload_to='images/%Y/%m/%d',
                          variations={'thumbnail': (600, 600)}
                         )

    created_by = models.ForeignKey(User, related_name='created_by')
    approved_by = models.ManyToManyField(User, blank=True, related_name='approved_by')
    date_filed = models.DateTimeField('date filed')
    status = models.CharField(max_length=2, choices=STATUS)

    def approved(self):
        return self.status == Item.PREAPPROVED

    def processed(self):
        return self.status == Item.PROCESSED

    def rejected(self):
        return self.status == Item.REJECTED

    def new(self):
        return self.status == Item.NEW

    def statusText(self):
        return dict(Item.STATUS)[self.status]

    def comName(self):
        return self.committee.name

    def __str__(self):
        return self.committee.name + ": " + self.event + " " + self.desc

    def mail_com_chair(self):
        send_mail(
            'New Reimbursement - ' + self.event + ': ' + self.desc,
            'Hey ' + self.committee.chair.first_name + ',\n\n' + \
            'Please take a moment to review http://fincom.delt.space/items/' + \
            str(self.pk) + ' and approve or reject the request from ' + \
            self.created_by.first_name + ' ' + self.created_by.last_name + \
            '. If you have any questions, contact the treasurer.\n\n' + \
            'Have a fiscally responsible day,\n Fincom Bot',
            'fincom.bot@gmail.com',
            [self.committee.chair.email],
            html_message='Hey ' + self.committee.chair.first_name+',<br><br>' +\
            'Please take a moment to review ' + \
            '<a href="http://fincom.delt.space/items/' + \
            str(self.pk) + '">http://fincom.delt.space/items/' + str(self.pk) +\
            '</a> and approve or reject the request from ' + \
            self.created_by.first_name + ' ' + self.created_by.last_name + \
            '. If you have any questions, contact the treasurer.<br><br>' + \
            'Have a fiscally responsible day,<br><br><em>Fincom Bot</em>'
        )

    def mail_fincom(self):
        emails = [s.email for s in User.objects.filter(groups__name='Fincom')]

        send_mail(
            'Preapproved Reimbursement - ' + self.event + ': ' + self.desc,
            'Hey Fincom,\n\n' + \
            'Please take a moment to review http://fincom.delt.space/items/' + \
            str(self.pk) + ' and approve or reject the request from ' + \
            self.created_by.first_name + ' ' + self.created_by.last_name + \
            '.\n\nHave a fiscally responsible day,\n Fincom Bot',
            'fincom.bot@gmail.com',
            emails,
            html_message='Hey Fincom,<br><br>' + \
            'Please take a moment to review ' + \
            '<a href="http://fincom.delt.space/items/' + \
            str(self.pk) + '">http://fincom.delt.space/items/' + str(self.pk) +\
            '</a> and approve or reject the request from ' + \
            self.created_by.first_name + ' ' + self.created_by.last_name + \
            '.<br><br>' + \
            'Have a fiscally responsible day,<br><br> <em>Fincom Bot</em>'
        )

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
