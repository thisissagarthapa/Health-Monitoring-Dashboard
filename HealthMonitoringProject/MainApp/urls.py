from django.urls import path
from .views import health,feature,working,testimonials,security,register,log_in,log_out,dashboard,overview,dataEntry,healthHistory ,Health_report ,generate_report,recommendation
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',health,name='health'),
    path('feature/',feature,name='feature'),
    path('working/',working,name='working'),
    path('testimonials/',testimonials,name='testimonials'),
    path('security/',security,name='security'),
    path('dashboard/',dashboard,name='dashboard'),
    path('overview/',overview,name='overview'),
    path('dataentry/',dataEntry,name='dataentry'),
    path('healthhistory/',healthHistory,name='healthhistory'),
    path('Health_report/',Health_report,name='Health_report'),
    path('report/<int:data_entry_id>/', generate_report, name='generate_report'),
    path('recommendation/',recommendation,name="recommendation"),      
]


# For  Authentication and Authorization
urlpatterns2 = [
path('register/',register,name="register"),
path('login/',log_in,name="log_in"),
path('logout/',log_out,name="log_out"),

# forget password setup
path("password_reset/", auth_views.PasswordResetView.as_view(template_name='Auth/password_reset.html'), name="password_reset"),
path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name='Auth/password_reset_done.html'), name="password_reset_done"),
path("password_reset_confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name='Auth/password_reset_confirm.html'), name="password_reset_confirm"),
path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name='Auth/password_reset_complete.html'), name="password_reset_complete"),
]

urlpatterns.extend(urlpatterns2)