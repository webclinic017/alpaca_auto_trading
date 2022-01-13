import uuid
from django.db import models, IntegrityError
from django.utils import timezone

class BaseTimeStampModel(models.Model):
    created = models.DateTimeField(editable=True)
    updated = models.DateTimeField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone.now()

        self.updated = timezone.now()
        return super(BaseTimeStampModel, self).save(*args, **kwargs)
    
class BaseTimeStampUidModel(BaseTimeStampModel):
    uid = models.UUIDField(primary_key=True, editable=False, unique=True)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4().hex
            success = False
            failures = 0
            while not success:
                try:
                    super(BaseTimeStampUidModel, self).save(*args, **kwargs)
                except IntegrityError:
                    failures += 1
                    if failures > 5:
                        raise KeyError
                    else:
                        self.uid = uuid.uuid4().hex
                else:
                    success = True
        else:
            super().save(*args, **kwargs)

class BaseUidModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, unique=True)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4().hex
            success = False
            failures = 0
            while not success:
                try:
                    super(BaseTimeStampUidModel, self).save(*args, **kwargs)
                except IntegrityError:
                    failures += 1
                    if failures > 5:
                        raise KeyError
                    else:
                        self.uid = uuid.uuid4().hex
                else:
                    success = True
        else:
            super().save(*args, **kwargs)