from django.db import models

class TestModel(models.Model):
  is_boolean = models.BooleanField(default=False)