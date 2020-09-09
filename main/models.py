from datetime import date

from django.conf import settings
from django.db import models


# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
def user_directory_path(instance, filename):
    td = date.today().strftime('%Y%m%d')
    return 'res{0}/{1}/{2}'.format(instance.upload.user.id, td, filename)


class Upload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=16, db_index=True)
    hash_secure = models.CharField(max_length=16, blank=True, db_index=True)
    password = models.CharField(max_length=20, blank=True)  # insecure


class Document(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE,
                               related_name='files')
    doc = models.FileField(upload_to=user_directory_path)

