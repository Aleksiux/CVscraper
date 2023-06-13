from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='cv', permanent=False)),
    path('index', views.index, name='index'),
    path('cv', views.all_cvs, name='cv'),
    path('cv/scrape_data', views.scrape_data, name='scrape_data'),
    path("cv/add_to_like_section", views.add_to_like_section, name="add_like"),
    path("cv/remove_from_like_section", views.remove_from_like_section, name="remove_like"),
    path('cv/liked_cvs', views.liked_cvs, name='liked_cvs'),
]
