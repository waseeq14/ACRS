from django.urls import path
from . import views

urlpatterns = [
    path('', views.run_analysis, name='run-analysis'),
    path('patch/', views.apply_patch, name='apply-patch'),
    path('exploit/', views.generate_exploit_path, name='generate-exploit-path'),
    path('file-save/', views.file_save, name="file-save"),
    path('pentest-scan/', views.pentest_scan, name="pentest-scan"),
    path('pentest-exploit/', views.pentest_scan_exploit, name="pentest-scan-exploit"),
    path('pentest-patch/', views.pentest_scan_patch, name="pentest-scan-patch"),
    path('register/', views.register_user, name="register"),
    path('projects/', views.fetch_projects, name='fetch-projects'),
    path('load-pentest-project/', views.load_pentest_project, name='load-pentest-project'),
    path('load-project/', views.load_project, name='load-project'),
    path('login/', views.login_user, name="login"),
    path('is-authenticated/', views.is_authenticated, name="is-authenticated"),
    path('logout/', views.logout_user, name='logout'),
    path('update-password/', views.change_password, name='update-password'),
    path('get-csrf-token/', views.csrf_token_view),
    path('get-pentest-report/', views.get_pentest_report, name='get-pentest-report'),
    path('get-dashboard-stats/', views.load_dashboard_stats, name='load-dashboard-stats'),
    path('get-report/', views.get_report, name='get-report'),
    path('fetch-reports/', views.fetch_reports, name='fetch-reports'),
    path('delete-report/', views.delete_report, name='delete-report'),
    path('delete-pentest-report/', views.delete_pentest_report, name='delete-pentest-report')
]