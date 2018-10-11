from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    pwd = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False)

    def get_name(self):
        return self.name
