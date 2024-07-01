from django.db import models


# Create your models here.
class Encryption(models.Model):
    passkey = models.CharField(max_length=100)
    encrypted_message = models.TextField()
    image = models.ImageField(upload_to='encrypted_images/')
    created_at = models.DateTimeField(auto_now_add=True)


class Decryption(models.Model):
    passkey = models.CharField(max_length=100)
    image = models.ImageField(upload_to='decryption_images/')
    created_at = models.DateTimeField(auto_now_add=True)