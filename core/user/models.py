from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import AppUserManager
import uuid
import base64

def generate_balance_id():
    r_id = base64.b64encode(uuid.uuid4().bytes).replace("=", "").decode()
    return r_id


def usermanagerprofile(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "{0}_manager_profile_pic/{1}".format(instance.username, filename)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(("email address"),null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    trade_status = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "username"
    AUTH_FIELD_NAME = "email"
    REQUIRED_FIELDS = ["email"]

    objects = AppUserManager()



    


    