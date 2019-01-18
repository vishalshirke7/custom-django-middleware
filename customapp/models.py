import binascii
import os

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


@python_2_unicode_compatible
class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

