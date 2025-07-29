from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    verb      = models.CharField(max_length=255)  # p.e. "tienes un nuevo pedido"
    data      = models.JSONField(blank=True,null=True)
    read      = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class InternalMessage(models.Model):
    sender    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_msgs')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recv_msgs')
    subject   = models.CharField(max_length=200)
    body      = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read      = models.BooleanField(default=False)
