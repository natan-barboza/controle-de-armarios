from django.contrib import admin
from apps.users.models import Users
from django.contrib.auth.models import User, Group
import logging

logger = logging.getLogger('custom')

class CustomUserAdmin(admin.ModelAdmin):
    def log_addition(self, request, object, message):
        super().log_addition(request, object, message)
        logger.info(f"Admin criou usuário: {object.username}")

    def log_change(self, request, object, message):
        super().log_change(request, object, message)
        logger.info(f"Admin editou usuário: {object.username}")

    def log_deletion(self, request, object, object_repr):
        super().log_deletion(request, object, object_repr)
        logger.info(f"Admin excluiu usuário: {object_repr}")

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, CustomUserAdmin)
admin.site.register(Users)