from django.contrib import admin
from .models import CabinetsManager, EmployeeExit, CabinetsManagerHistory, EmployeeExitHistory

class CabinetsManagerAdmin(admin.ModelAdmin):
    list_display = ("cabinet_id", "owner", "initial_datetime", "final_datetime")
class CabinetsManagerHistoryAdmin(admin.ModelAdmin):
    list_display = ("cabinet_id", "owner", "initial_datetime", "final_datetime")

class EmployeeExitAdmin(admin.ModelAdmin):
    list_display = ("cabinet", "user", "authorized")
class EmployeeExitHistoryAdmin(admin.ModelAdmin):
    list_display = ("cabinet", "user", "authorized")

admin.site.register(CabinetsManager, CabinetsManagerAdmin)
admin.site.register(CabinetsManagerHistory, CabinetsManagerHistoryAdmin)
admin.site.register(EmployeeExit, EmployeeExitAdmin)
admin.site.register(EmployeeExitHistory, EmployeeExitHistoryAdmin)