from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    image = models.ImageField(upload_to="users_images/", null=True, blank=True)
    phone = models.CharField(max_length=25, null=False, blank=False)

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id',]

    def __str__(self):
        return f'id: {self.id}, User name: {self.username}, email: {self.email}'