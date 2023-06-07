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
    context = {
        # 'cvbankas': cvbankas_lt('kaunas', 'python'),
        # 'count': len(cvbankas_lt('kaunas', 'python'))
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
        cv_forms = []
        for work_key, work_value in work_categories.items():
            for work_data in cvbankas_lt(work=work_key):
                cv_form = CvForm(
                    logo_url=work_data['logo'],
                    position=work_data['position'],
                    employer=work_data['employer'],
                    salary=work_data['salary'],
                    salary_taxes=work_data['salary_taxes'],
                    city=work_data['location'],
                    how_old_ad=work_data['how_old_ad'],
                    ad_link=work_data['ad_link'],
                    work_area=work_key
                )
                cv_forms.append(cv_form)
    return render(request, 'all_cvs.html')
