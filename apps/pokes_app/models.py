from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def validate_reg(self, postData):
        errors = {}
        my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['name']) < 2:
            errors['name'] = "Please enter a name with at least 2 characters"

        if len(postData['alias']) < 2:
            errors['alias'] = "Please enter an alias with at least 2 characters"

        if not my_re.match(postData['email']):
            errors['email'] = "Please enter your email in a valid format"

        if postData['password'] != postData['password_confirm']:
            errors['password'] = "Your password and its confirmation do not match"

        return errors

    def validate_log(self, postData):
        errors = {}
        my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        hash2 = postData['password'].encode()

        if not my_re.match(postData['email']):
            errors['email'] = "Please enter your email in a valid format"

        if not bcrypt.checkpw(hash2, postData['hash1'].encode()):
            errors['password'] = "Please enter the correct password associated with this account"

        return errors


class User(models.Model):
    name = models.CharField(max_length=30)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=255)
    poke_history = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Poke(models.Model):
    user = models.ForeignKey(User, related_name='pokes', null=True, blank=True)
    receiver = models.ForeignKey(User, related_name='pokes_received', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

