import json

from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponse

from .utils import cvbankas_lt
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CvForm, Profile

WORK_CATEGORIES = {
    'it': 'IT',
    'administration': 'Administration',
    'production': 'Production',
    'medicine': 'Medicine',
    'transport_driving': 'Transport/Driving'
}

CITY = {
    'Kaune': 'Kaunas',
    'Vilniuje': 'Vilnius',
    'Klaipėdoje': 'Klaipeda',
    'Alytuje': 'Alytus',
    'Birštone': 'Birstonas',
    'Jonavoje': 'Jonava',
    'Darbas namuose': 'Darbas namuose',
}


def index(request):
    context = {
    }
    return render(request, "index.html", context)


def all_cvs(request):
    cvs = CvForm.objects.all()
    if request.method == "POST":
        selected_cities = request.POST.getlist('selected_city')
        selected_speciality = request.POST.getlist('selected_job')
        if not selected_cities:
            selected_cities = list(CITY.keys())
        if not selected_speciality:
            selected_speciality = list(WORK_CATEGORIES.keys())
        search_results = CvForm.objects.filter(Q(city__in=selected_cities) & Q(work_area__in=selected_speciality))
        context = {
            'cvs': search_results,
            'selected_speciality': selected_speciality,
            'selected_cities': selected_cities,
        }
        return render(request, "all_cvs.html", context=context)
    context = {
        'cvs': cvs,
    }
    return render(request, "all_cvs.html", context=context)


def is_admin(user):
    return user.is_superuser


@login_required  # Ensures that the user is logged in
@user_passes_test(is_admin)  # Restricts access to admin users
def scrape_data(request):
    if request.method == "POST":
        for work_key, work_value in WORK_CATEGORIES.items():
            for work_data in cvbankas_lt(work=work_key):
                cv_form_data = {
                    'logo_url': work_data['logo'],
                    'position': work_data['position'],
                    'employer': work_data['employer'],
                    'salary': work_data['salary'],
                    'salary_taxes': work_data['salary_taxes'],
                    'city': work_data['location'],
                    'how_old_ad': work_data['how_old_ad'],
                    'ad_link': work_data['ad_link'],
                    'work_area': work_key
                }
                try:
                    cv_form = CvForm.objects.get(ad_link=work_data['ad_link'])
                except CvForm.DoesNotExist:
                    cv_form = CvForm(
                        logo_url=cv_form_data['logo_url'],
                        position=cv_form_data['position'],
                        employer=cv_form_data['employer'],
                        salary=cv_form_data['salary'],
                        salary_taxes=cv_form_data['salary_taxes'],
                        city=cv_form_data['city'],
                        how_old_ad=cv_form_data['how_old_ad'],
                        ad_link=cv_form_data['ad_link'],
                        work_area=cv_form_data['work_area']
                    )
                    cv_form.save()
                else:
                    for field, value in cv_form_data.items():
                        if getattr(cv_form, field) != value:
                            setattr(cv_form, field, value)
                    cv_form.save()
    return render(request, 'all_cvs.html')


def add_to_like_section(request):
    data = json.loads(request.body)
    cv_id = data["cv_id"]
    cv = CvForm.objects.get(cv_id=cv_id)

    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.likes.add(cv)
        profile.save()

        like_section_data = {
            "id": profile.profile_id,
            "user": profile.user.username,
            "likes": [cv.cv_id],
        }

        return JsonResponse(like_section_data, safe=False)


def remove_from_like_section(request):
    data = json.loads(request.body)
    cv_id = data["cv_id"]
    cv = CvForm.objects.get(cv_id=cv_id)

    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.likes.remove(cv)
        profile.save()

        like_section_data = {
            "id": profile.profile_id,
            "user": profile.user.username,
            "likes": [cv.cv_id],
        }

        return JsonResponse(like_section_data, safe=False)


def liked_cvs(request):
    profile = Profile.objects.get(user=request.user)
    cv_forms = profile.likes.all()
    context = {
        'cvs': cv_forms
    }
    return render(request, 'liked_cvs.html', context=context)
