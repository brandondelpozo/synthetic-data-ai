from django.contrib import admin
from .models import DynamicTableDefinition, DynamicTableExport

@admin.register(DynamicTableDefinition)
class DynamicTableDefinitionAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'table_name', 'is_migrated', 'created_at']
    list_filter = ['is_migrated', 'created_at']
    search_fields = ['display_name', 'table_name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(DynamicTableExport)
class DynamicTableExportAdmin(admin.ModelAdmin):
    list_display = ['id', 'table_definition', 'num_records', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at', 'table_definition']
    readonly_fields = ['created_at', 'completed_at']
