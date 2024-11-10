import datetime
import random
from hashids import Hashids
from django.db import models
from django.utils.translation import gettext_lazy as _


def create_unique_hash(model, instance):
    """
    Generates a unique hash ID for model instances
    """
    while True:
        raw_salt = f'{model._meta.db_table}{instance.pk}{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'
        salt = ''.join(random.sample(raw_salt, len(raw_salt)))
        hash_id = Hashids(salt=salt, min_length=16).encode(instance.pk)
        if hash_id:
            try:
                model.objects.get(hash_id=hash_id)
            except model.DoesNotExist:
                return hash_id


class LogicalDeleteQuerySet(models.QuerySet):
    """
    Custom QuerySet for logical deletion
    """
    def logical_delete(self):
        self.update(deleted_at=datetime.datetime.now())


class LogicalDeleteManager(models.Manager):
    """
    Manager for handling logical deletion
    """
    def get_queryset(self):
        return LogicalDeleteQuerySet(self.model).filter(deleted_at=None)


class HashIDManager(models.Manager):
    """
    Manager for handling hash ID generation
    """
    def create(self, **obj_data):
        instance = super().create(**obj_data)
        instance.hash_id = create_unique_hash(self.model, instance)
        instance.save()
        return instance


class TaskManagerBaseModel(models.Model):
    """
    Base model with timestamp fields and logical deletion
    """
    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = LogicalDeleteManager()
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        """
        Custom save method to handle timestamp updates
        """
        auto_now = kwargs.pop('updated_at_auto_now', True)
        if auto_now:
            self.updated_at = datetime.datetime.now()
        super().save(*args, **kwargs)

    def logical_delete(self):
        """
        Performs logical deletion of the instance
        """
        self.deleted_at = datetime.datetime.now()
        self.save()


class HashIDModel(TaskManagerBaseModel):
    """
    Model with hash ID functionality
    """
    class Meta:
        abstract = True

    hash_id = models.CharField(max_length=50, unique=True)
    objects = HashIDManager()
