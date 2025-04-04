from django.contrib import admin
from apps.cabinets.models import Cabinets

class CabinetsAdmin(admin.ModelAdmin):
    list_display = ("cabinet", "status", "reserved")

admin.site.register(Cabinets, CabinetsAdmin)
