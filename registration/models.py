from django.db import models


class User(models.Model):
    username = models.CharField(max_length=10)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.TextField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
