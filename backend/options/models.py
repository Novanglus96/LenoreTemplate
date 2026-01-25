from django.db import models
from django.core.exceptions import ValidationError
import pytz
import os

# Create your models here.


class SingletonModel(models.Model):
    """
    Class for repersenting a Singleton model.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Overides the save to make sure there is only one instance of this model.

        Raises:
            ValidationError: A string stating there is already an instance of this
            model.

        Returns:
            (SingletonModel): The singleton model.
        """
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError("There is already one instance of this model")
        return super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Overrides delete so that you can not delete the singleton model.

        Raises:
             ValidationError: A string stating you can't delete this object.
        """
        raise ValidationError("You cannot delete this object")


class Version(SingletonModel):
    """
    Model representing app version.

    Attributes:
        version_number (CharField): The current version of the app.
    """

    version_number = models.CharField(max_length=25)

    def __str__(self):
        """
        __str__ Overrides the string representation for Version and returns the
        version number.

        Returns:
            (str): The string representation of the version number.
        """
        return self.version_number
