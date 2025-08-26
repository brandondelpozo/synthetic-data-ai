from django.db import models
from django.contrib.auth.models import User
import json


class DynamicTableDefinition(models.Model):
    """Model to store dynamic table definitions created by users"""
    table_name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fields_definition = models.JSONField(help_text="JSON containing field definitions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_migrated = models.BooleanField(default=False)
    migration_file = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.display_name} ({self.table_name})"


class DynamicTableExport(models.Model):
    """Model to track Excel exports of dynamic tables"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    table_definition = models.ForeignKey(DynamicTableDefinition, on_delete=models.CASCADE, related_name='exports')
    num_records = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    file_path = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Export #{self.id} - {self.table_definition.display_name} ({self.num_records} records)"
