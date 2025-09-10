from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class ScrapedEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.EmailField()
    subject = models.CharField(max_length=500)
    snippet = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=50, blank=True, null=True)  #ex coupons trials subscritipons (labelling)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, default='other')
    
    def __str__(self):
        return self.subject