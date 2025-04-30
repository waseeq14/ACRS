from django.urls import path
from .views import (
    run_analysis,
    file_save,
    register_user,
    login_user,
    is_authenticated,
    logout_user,
    change_password,
    apply_patch,
    generate_exploit_path,
    pentest_scan,
    pentest_scan_exploit,
    pentest_scan_patch,
    csrf_token_view,
    fetch_projects,
    load_pentest_projects
)

urlpatterns = [
    path('', run_analysis, name='run-analysis'),
    path('patch/', apply_patch, name='apply-patch'),
    path('exploit/', generate_exploit_path, name='generate-exploit-path'),
    path('file-save/', file_save, name="file-save"),
    path('pentest-scan/', pentest_scan, name="pentest-scan"),
    path('pentest-exploit/', pentest_scan_exploit, name="pentest-scan-exploit"),
    path('pentest-patch/', pentest_scan_patch, name="pentest-scan-patch"),
    path('register/', register_user, name="register"),
    path('projects/', fetch_projects, name='fetch-projects'),
    path('load-pentest-projects/', load_pentest_projects, name='load-pentest-projects'),
    path('login/', login_user, name="login"),
    path('is-authenticated/', is_authenticated, name="is-authenticated"),
    path('logout/', logout_user, name='logout'),
    path('update-password/', change_password, name='update-password'),
    path('get-csrf-token/', csrf_token_view),
]