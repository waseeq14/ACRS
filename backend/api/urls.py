from django.urls import path
from .  import run_analysis

urlpatterns = [
    path('', run_analysis, name='run-analysis'),
]