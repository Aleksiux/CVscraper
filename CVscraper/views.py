from .utils import cvbankas_lt
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    context = {
    }
    return render(request, "index.html", context)


def all_cvs(request):
    context = {
        'cvbankas': cvbankas_lt('kaunas', 'python'),
        'count': len(cvbankas_lt('kaunas', 'python'))
    }
    return render(request, "all_cvs.html", context=context)


def is_admin(user):
    return user.is_superuser


@login_required  # Ensures that the user is logged in
@user_passes_test(is_admin)  # Restricts access to admin users
def scrape_data(request):
    return render(request, 'all_cvs.html')
