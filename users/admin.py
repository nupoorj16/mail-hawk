from django.contrib import admin
from .models import ScrapedEmail #type:ignore

# Register your models here.
admin.site.register(ScrapedEmail)