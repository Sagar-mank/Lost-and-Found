from django.contrib import admin
from .models import LostItem, FoundItem, Claim

admin.site.register(LostItem)
admin.site.register(FoundItem)
admin.site.register(Claim)