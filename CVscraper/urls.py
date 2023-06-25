from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('index', views.index, name='index'),
    path('', RedirectView.as_view(url='login/', permanent=False)),
    path('cv/', views.all_cvs, name='cv'),
    path('cv/<int:page>/', views.all_cvs, name='list_cvs'),
    path('cv/scrape_data', views.scrape_data, name='scrape_data'),
    path("cv/add_to_like_section", views.add_to_like_section, name="add_like"),
    path("cv/remove_from_like_section", views.remove_from_like_section, name="remove_like"),
    path('cv/liked_cvs', views.liked_cvs, name='liked_cvs'),
    path('account/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('reset-password/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
