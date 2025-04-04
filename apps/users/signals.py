import logging
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

logger = logging.getLogger('custom')

@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Usuário criado: {instance.username} (ID: {instance.id})")
    else:
        logger.info(f"Usuário editado: {instance.username} (ID: {instance.id})")

@receiver(post_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    logger.info(f"Usuário excluído: {instance.username} (ID: {instance.id})")

@receiver(post_save, sender=Group)
def log_group_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Grupo criado: {instance.name} (ID: {instance.id})")
    else:
        logger.info(f"Grupo editado: {instance.name} (ID: {instance.id})")

@receiver(post_delete, sender=Group)
def log_group_delete(sender, instance, **kwargs):
    logger.info(f"Grupo excluído: {instance.name} (ID: {instance.id})")
