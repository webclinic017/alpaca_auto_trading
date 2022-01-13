from django.db import models
from django.utils import timezone
from django.db import IntegrityError
import uuid

class BaseTimeStampModel(models.Model):
    """
    Base model for timestamp support, related models: :model:`Clients.Client` and its related models, :model:`orders.Order` etc.
    """
    created = models.DateTimeField(editable=True)
    updated = models.DateTimeField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone.now()

        self.updated = timezone.now()
        return super(BaseTimeStampModel, self).save(*args, **kwargs)
    

class TimestampWithUid(BaseTimeStampModel):
    uid = models.CharField(primary_key=True, editable=False,max_length=255)
    
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4().hex
            # using your function as above or anything else
            success = False
            failures = 0
            while not success:
                try:
                    super(TimestampWithUid, self).save(*args, **kwargs)
                except IntegrityError:
                    failures += 1
                    if failures > 5:  # or some other arbitrary cutoff point at which things are clearly wrong
                        raise KeyError
                    else:
                        # looks like a collision, try another random value
                        self.uid = uuid.uuid4().hex
                else:
                    success = True
        else:
            super().save(*args, **kwargs)