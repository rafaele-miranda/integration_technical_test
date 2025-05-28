from django.db import models
from django.utils import timezone
from datetime import datetime
import pytz

class WorkOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled')
    ]
    
    number = models.IntegerField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_synced = models.BooleanField(default=False)
    synced_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ordem #{self.number} - {self.status}"