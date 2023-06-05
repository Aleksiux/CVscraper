from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('cv', views.all_cvs, name='cv'),
    path('cv/scrape_data', views.scrape_data, name='scrape_data'),
]
