from random import randint
from django.db import models



class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RandomNameGeneratedModel(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True,
        blank=True, )

    def generate_name(self):
        pass

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.name == "" or self.name is None:
            generated_name = self.generate_name()
            assert generated_name is not None, f"You must implement generate_name() function " \
                                               f"in {self._meta.model_name} model."
            self.name = generated_name

        super(RandomNameGeneratedModel, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True
