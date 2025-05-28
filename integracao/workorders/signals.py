# workorders/signals.py
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import WorkOrder
import json
import os

@receiver(post_save, sender=WorkOrder)
def handle_outbound_sync(sender, instance, created, **kwargs):
    if not instance.is_synced:
        
        # Marcar como sincronizado
        instance.is_synced = True
        instance.synced_at = timezone.now() 
        instance.save(update_fields=['is_synced', 'synced_at'])
        
        client_data = {
            'orderNo': instance.number,
            'isPending': instance.status == 'pending',
            'isOnHold': instance.status == 'on_hold',
            'isDone': instance.status == 'completed',
            'isCanceled': instance.status == 'cancelled',
            'summary': instance.title,
            'creationDate': instance.created_at.isoformat() if instance.created_at else None,
            'lastUpdateDate': instance.updated_at.isoformat() if instance.updated_at else None,
            'isSynced': instance.is_synced,
            'syncDate': instance.synced_at.isoformat() if instance.synced_at else None
        }
        
        
        # Salvar arquivo JSON
        with open(f"{settings.DATA_OUTBOUND_DIR}/{instance.number}.json", 'w') as f:
            json.dump(client_data, f)
        
        