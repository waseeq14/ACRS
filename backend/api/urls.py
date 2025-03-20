from django.urls import path
from .views import run_analysis, file_save, register_user, login_user, is_authenticated, logout_user

urlpatterns = [
    path('', run_analysis, name='run-analysis'),
    path('file-save/', file_save, name="file-save"),
    path('register/', register_user, name="register"),
    path('login/', login_user, name="login"),
    path('is-authenticated/', is_authenticated, name="is-authenticated"),
    path('logout/', logout_user, name='logout')
]