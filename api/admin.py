from django.contrib import admin
from .models import Petition, Signature

# Register your models here.

admin.site.register(Petition)
admin.site.register(Signature)
