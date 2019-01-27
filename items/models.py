from __future__ import unicode_literals
from __future__ import with_statement

from datetime import datetime, date
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.template import loader
from io import BytesIO
from PIL import Image
from storages.backends.s3boto3 import S3Boto3Storage
from stdimage.models import StdImageField
from stdimage.utils import render_variations

from committee.models import Committee

from django.db import models

#EXIF key index for the orientation value
ORIENTATION_KEY = 274
ROTATE_VALUES = {
    3: Image.ROTATE_180,
    6: Image.ROTATE_270,
    8: Image.ROTATE_90,
}

# helper to fix "soft" rotated images
def resizeAndRotate(file_name, variations, storage):
    rotated = False
    with storage.open(file_name) as f:
        try:
            image = Image.open(f)
        except:
            return False
        else:
            with image:
                try:
                    file_format = image.format
                    exif = image._getexif()

                    if exif and ORIENTATION_KEY in exif:
                        orientation = exif[ORIENTATION_KEY]

                        if orientation in ROTATE_VALUES:
                            image = image.transpose(ROTATE_VALUES[orientation])
                            rotated = True

                    if rotated:
                        with BytesIO() as file_buffer:
                            image.save(file_buffer, file_format)
                            f = ContentFile(file_buffer.getvalue())
                            storage.delete(file_name)
                            storage.save(file_name, f)
                except:
                    return True

    render_variations(file_name, variations, storage=storage)
    return False

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
    committee = models.ForeignKey(Committee, on_delete=models.DO_NOTHING)
    details = models.TextField()
    cost = models.DecimalField(max_digits=7, decimal_places=2)
    date_purchased = models.DateField('date purchased')
    image = StdImageField(upload_to='images/%Y/%m/%d',
                          render_variations=resizeAndRotate,
                          variations={'thumbnail': (600, 600)}
                         )

    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.DO_NOTHING)
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
        template = loader.get_template('items/item-email.html')
        context_plain = {
            'I': self,
            'to': self.committee.chair.first_name,
            'submitter': self.created_by.first_name + ' ' + self.created_by.last_name,
        }
        context_html = {
            'I': self,
            'to': self.committee.chair.first_name,
            'submitter': self.created_by.first_name + ' ' + self.created_by.last_name,
            'html': True,
        }

        send_mail(
            'New Reimbursement - ' + self.event + ': ' + self.desc,
            template.render(context_plain),
            'fincom.bot@gmail.com',
            [self.committee.chair.email],
            html_message=template.render(context_html),
        )

    def mail_fincom(self):
        emails = [s.email for s in User.objects.filter(groups__name='Fincom')]

        template = loader.get_template('items/item-email.html')
        context_plain = {
            'I': self,
            'to': 'Fincom',
            'submitter': self.created_by.first_name + ' ' + self.created_by.last_name,
        }
        context_html = {
            'I': self,
            'to': 'Fincom',
            'submitter': self.created_by.first_name + ' ' + self.created_by.last_name,
            'html': True,
        }

        send_mail(
            'Preapproved Reimbursement - ' + self.event + ': ' + self.desc,
            template.render(context_plain),
            'fincom.bot@gmail.com',
            emails,
            html_message=template.render(context_html),
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
