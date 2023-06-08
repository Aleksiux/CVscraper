from .utils import cvbankas_lt
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CvForm


def index(request):
    context = {
    }
    return render(request, "index.html", context)


def all_cvs(request):
    cvs = CvForm.objects.all()
    if request.method == "POST":
        selected_cities = request.POST.getlist('selected_city')
        search_results = CvForm.objects.filter(city__in=selected_cities)
        context = {
            'cvs': search_results
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
        work_categories = {
            'it': 'IT',
            'administration': 'Administration',
            'production': 'Production',
            'medicine': 'Medicine',
            'transport_driving': 'Transport/Driving'
        }
        for work_key, work_value in work_categories.items():
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
