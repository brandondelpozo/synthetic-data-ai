from django.urls import path
from . import views

urlpatterns = [
    # Home page is now the Model Builder
    path('', views.home, name='home'),
    
    # Dynamic Model Builder URLs
    path('add-field/', views.add_field, name='add_field'),
    path('create/', views.create_dynamic_table, name='create_dynamic_table'),
    path('tables/', views.dynamic_table_list, name='dynamic_table_list'),
    path('table/<int:table_id>/', views.dynamic_table_detail, name='dynamic_table_detail'),
    path('table/<int:table_id>/generate-excel/', views.generate_excel_data, name='generate_excel_data'),
    path('progress/<int:export_id>/', views.progress_status, name='progress_status'),
    path('progress/<int:export_id>/complete/', views.progress_complete, name='progress_complete'),
    path('excel-export/<int:export_id>/download/', views.download_excel, name='download_excel'),
]
