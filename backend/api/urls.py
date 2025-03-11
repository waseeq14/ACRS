from django.urls import path
from .views import run_analysis, file_save

urlpatterns = [
    path('', run_analysis, name='run-analysis'),
    path('file-save/', file_save, name="file-save")
]