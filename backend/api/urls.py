from django.urls import path
from .views import run_analysis

urlpatterns = [
    path('', run_analysis, name='run-analysis'),
]