from authtools.models import AbstractEmailUser
from django.db import models
from django.urls import reverse


class UserProfile(AbstractEmailUser):
    user_email = models.EmailField(verbose_name='User Email', max_length=100)
    username = models.CharField(verbose_name='Username', max_length=250, blank=True, null=True)
    password = models.CharField(verbose_name='Password', max_length=255)
    image = models.ImageField(upload_to='media', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('cabinet', kwargs={'pk': self.objects.pk})

    def __str__(self):
        return self.email

