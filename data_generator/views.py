from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import DynamicTableDefinition, DynamicTableExport, GenerationProgress
from .dynamic_models import DynamicModelGenerator
import json
import random
from datetime import datetime
import csv
import os
from django.conf import settings

def home(request):
    """Main page - Model Builder interface"""
    tables = DynamicTableDefinition.objects.all().order_by('-created_at')
    return render(request, 'data_generator/model_builder.html', {'tables': tables})


# Dynamic Model Builder Views

@csrf_exempt
def add_field(request):
    """HTMX endpoint to add a new field to the form"""
    if request.method == 'GET':
        field_index = request.GET.get('index', 0)
        return render(request, 'data_generator/field_form.html', {'field_index': field_index})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt 
@require_POST
def create_dynamic_table(request):
    """Process the dynamic table creation form"""
    try:
        # Parse form data
        table_name = request.POST.get('table_name', '').lower().replace(' ', '_')
        display_name = table_name.replace('_', ' ').title()  # Generate display name from table name
        description = request.POST.get('description', '')
        
        if not table_name:
            return JsonResponse({'error': 'Table name is required'}, status=400)
        
        # Collect field definitions
        fields_definition = []
        field_index = 0
        
        while f'field_{field_index}_name' in request.POST:
            field_name = request.POST.get(f'field_{field_index}_name')
            field_type = request.POST.get(f'field_{field_index}_type')
            
            if not field_name or not field_type:
                field_index += 1
                continue
                
            field_def = {
                'name': field_name.lower().replace(' ', '_'),
                'type': field_type,
                'options': {}
            }
            
            # Add type-specific options
            if field_type == 'string':
                max_length = request.POST.get(f'field_{field_index}_max_length')
                if max_length:
                    field_def['options']['max_length'] = int(max_length)
                    
            elif field_type == 'number':
                min_value = request.POST.get(f'field_{field_index}_min_value')
                max_value = request.POST.get(f'field_{field_index}_max_value')
                if min_value:
                    field_def['options']['min_value'] = int(min_value)
                if max_value:
                    field_def['options']['max_value'] = int(max_value)
                    
            elif field_type == 'choice':
                choices_str = request.POST.get(f'field_{field_index}_choices', '')
                if choices_str:
                    choices = [choice.strip() for choice in choices_str.split(',') if choice.strip()]
                    field_def['options']['choices'] = choices
            
            # Add AI description if specified
            ai_description = request.POST.get(f'field_{field_index}_ai_description')
            if ai_description:
                field_def['options']['ai_description'] = ai_description
            
            # Add nullable option
            nullable = request.POST.get(f'field_{field_index}_nullable') == 'on'
            field_def['options']['nullable'] = nullable
            
            fields_definition.append(field_def)
            field_index += 1
        
        if not fields_definition:
            return JsonResponse({'error': 'At least one field is required'}, status=400)
        
        # Check if table name already exists before creating
        if DynamicTableDefinition.objects.filter(table_name=table_name).exists():
            return JsonResponse({'error': f'Table "{table_name}" already exists. Please choose a different name.'}, status=400)
        
        # Create table definition
        table_definition_data = {
            'table_name': table_name,
            'display_name': display_name,
            'description': description,
            'fields_definition': fields_definition
        }
        
        # Save to database
        table_def = DynamicTableDefinition.objects.create(
            table_name=table_name,
            display_name=display_name,
            description=description,
            fields_definition=fields_definition
        )
        
        # Create dynamic model and migration
        generator = DynamicModelGenerator()
        try:
            model_class = generator.create_model_class(table_definition_data)
            migration_file = generator.create_migration_file(table_definition_data, model_class)
            
            # Run migration with better error handling
            success, error_msg = generator.run_migration_with_feedback(migration_file)
            if success:
                table_def.is_migrated = True
                table_def.migration_file = migration_file
                table_def.save()
                
                messages.success(request, f'Table "{display_name}" created successfully!')
                return JsonResponse({
                    'success': True, 
                    'message': f'Table "{display_name}" created successfully!',
                    'redirect': f'/table/{table_def.id}/'
                })
            else:
                # Delete the table definition if migration failed
                table_def.delete()
                error_detail = error_msg if error_msg else 'Unknown migration error'
                messages.error(request, f'Failed to create database table: {error_detail}')
                return JsonResponse({'error': f'Failed to create database table: {error_detail}'}, status=500)
                
        except Exception as e:
            # Delete the table definition if there was an error
            try:
                table_def.delete()
            except:
                pass
            error_msg = str(e)
            messages.error(request, f'Error creating table: {error_msg}')
            return JsonResponse({'error': f'Error creating table: {error_msg}'}, status=500)
            
    except Exception as e:
        return JsonResponse({'error': f'Error processing request: {str(e)}'}, status=500)

def dynamic_table_detail(request, table_id):
    """View details of a dynamic table"""
    table_def = get_object_or_404(DynamicTableDefinition, pk=table_id)
    exports = table_def.exports.all()[:10]
    
    # Check if OpenAI API key is set in Django settings (from .env file)
    from django.conf import settings
    has_env_api_key = bool(getattr(settings, 'OPENAI_API_KEY', ''))
    
    context = {
        'table_def': table_def,
        'recent_exports': exports,
        'fields_json': json.dumps(table_def.fields_definition, indent=2),
        'has_env_api_key': has_env_api_key
    }
    return render(request, 'data_generator/dynamic_table_detail.html', context)

@require_POST
def generate_excel_data(request, table_id):
    """Generate synthetic data and export to Excel"""
    table_def = get_object_or_404(DynamicTableDefinition, pk=table_id)
    
    if not table_def.is_migrated:
        messages.error(request, 'Table has not been migrated yet')
        return redirect('dynamic_table_detail', table_id=table_id)
    
    num_records = int(request.POST.get('num_records', 5))
    openai_api_key = request.POST.get('openai_api_key', '').strip()
    
    # If no API key provided in form, try to get from Django settings (.env file)
    if not openai_api_key:
        from django.conf import settings
        openai_api_key = getattr(settings, 'OPENAI_API_KEY', '')
    
    if num_records > 10:
        messages.error(request, 'Maximum 10 records allowed per export')
        return redirect('dynamic_table_detail', table_id=table_id)
    
    # Create export record
    export = DynamicTableExport.objects.create(
        table_definition=table_def,
        num_records=num_records,
        status='processing'
    )
    
    # Create progress tracking
    progress = GenerationProgress.objects.create(
        export=export,
        current_step='initializing',
        progress_percentage=0,
        message='Starting data generation...'
    )
    
    try:
        # Update progress
        progress.current_step = 'generating_data'
        progress.progress_percentage = 20
        progress.message = 'Generating synthetic data...'
        progress.save()
        
        generator = DynamicModelGenerator()
        
        # Generate synthetic data
        table_definition_data = {
            'table_name': table_def.table_name,
            'display_name': table_def.display_name,
            'fields_definition': table_def.fields_definition
        }
        
        data = generator.generate_synthetic_data(table_definition_data, num_records, openai_api_key)
        
        # Update progress
        progress.current_step = 'creating_excel'
        progress.progress_percentage = 60
        progress.message = 'Creating Excel file...'
        progress.save()
        
        # Create Excel file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{table_def.table_name}_{timestamp}.xlsx"
        output_dir = os.path.join(settings.BASE_DIR, 'output')
        output_path = os.path.join(output_dir, filename)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        generator.create_excel_file(table_definition_data, data, output_path)
        
        # Update progress
        progress.current_step = 'saving_to_db'
        progress.progress_percentage = 80
        progress.message = 'Saving to database...'
        progress.save()
        
        # Optionally insert data into database
        if request.POST.get('save_to_db') == 'on':
            generator.insert_data_to_db(table_definition_data, data)
        
        # Update progress
        progress.current_step = 'completed'
        progress.progress_percentage = 100
        progress.message = 'Generation completed successfully!'
        progress.save()
        
        # Update export record
        export.status = 'completed'
        export.file_path = output_path
        export.completed_at = datetime.now()
        export.save()
        
        messages.success(request, f'Successfully generated {num_records} records and exported to Excel!')
        
        # Check if this is an HTMX request
        if request.headers.get('HX-Request'):
            # Return download link for HTMX
            return render(request, 'data_generator/download_link.html', {
                'export': export,
                'download_url': f'/excel-export/{export.id}/download/'
            })
        else:
            # Regular redirect for non-HTMX requests
            return redirect('download_excel', export_id=export.id)
        
    except Exception as e:
        progress.current_step = 'failed'
        progress.progress_percentage = 0
        progress.message = f'Error: {str(e)}'
        progress.save()
        
        export.status = 'failed'
        export.error_message = str(e)
        export.save()
        messages.error(request, f'Error generating data: {str(e)}')
        return redirect('dynamic_table_detail', table_id=table_id)

def progress_status(request, export_id):
    """HTMX endpoint to get progress status"""
    try:
        export = get_object_or_404(DynamicTableExport, pk=export_id)
        progress = export.progress
        
        return render(request, 'data_generator/progress_bar.html', {
            'progress': progress,
            'export': export
        })
    except GenerationProgress.DoesNotExist:
        return render(request, 'data_generator/progress_bar.html', {
            'progress': None,
            'export': None
        })

def download_excel(request, export_id):
    """Download generated Excel file"""
    export = get_object_or_404(DynamicTableExport, pk=export_id)
    
    if export.status != 'completed' or not export.file_path:
        messages.error(request, 'Export is not ready for download')
        return redirect('dynamic_table_detail', table_id=export.table_definition.id)
    
    if not os.path.exists(export.file_path):
        messages.error(request, 'Excel file not found')
        return redirect('dynamic_table_detail', table_id=export.table_definition.id)
    
    # Serve file
    with open(export.file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(export.file_path)}"'
        return response

def dynamic_table_list(request):
    """List all dynamic tables"""
    tables = DynamicTableDefinition.objects.all().order_by('-created_at')
    paginator = Paginator(tables, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'data_generator/dynamic_table_list.html', context)
