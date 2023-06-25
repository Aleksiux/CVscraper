import json
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_protect
from .utils import cvbankas_lt
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CvForm, Profile
from django.contrib import messages, auth
from django.contrib.auth.forms import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import UserUpdateForm, ProfileUpdateForm

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


def logout(request):
    auth.logout(request)
    return redirect(request, 'login')


@csrf_protect
def register(request):
    if request.method == "POST":
        # taking all values from registration form
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # checking if passwords matches
        if password != password2:
            messages.error(request, 'Password does not match!')
            return redirect('register')

        # checking if username is not taken
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username {username} is taken! Choose another one')
            return redirect('register')

        # checking if email is not taken
        if User.objects.filter(email=email).exists():
            messages.error(request, f'User with {email} is already registered!')
            return redirect('register')

        # if everything is good, create new user.
        User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                 password=password)
        messages.info(request, f'User with username {username} registered!')
        return redirect('login')
    return render(request, 'registration/register.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)


@login_required
def all_cvs(request):
    cvs = CvForm.objects.all()
    paginator = Paginator(CvForm.objects.all(), 100)
    page_number = request.GET.get('page')
    paged_cvs = paginator.get_page(page_number)
    if request.method == "POST":
        selected_cities = request.POST.getlist('selected_city')
        selected_speciality = request.POST.getlist('selected_job')
        search_input = request.POST.get('input_search')
        if not selected_cities:
            selected_cities = list(CITY.keys())
        if not selected_speciality:
            selected_speciality = list(WORK_CATEGORIES.keys())
        if search_input is None:
            search_input = ''
        search_results = CvForm.objects.filter(
            Q(position__icontains=search_input) & Q(city__in=selected_cities) & Q(work_area__in=selected_speciality))
        user_profile = Profile.objects.filter(user=request.user).values_list('likes', flat=True)
        paginator = Paginator(search_results, 100)
        page_number = request.GET.get('page')
        paged_cvs = paginator.get_page(page_number)
        context = {
            'user_profile': list(user_profile),
            'user': request.user,
            'cvs': paged_cvs,
            'count': cvs.count(),
            'selected_speciality': selected_speciality,
            'selected_cities': selected_cities,
        }
        return render(request, "all_cvs.html", context=context)
    selected_cities = list(CITY.keys())
    selected_speciality = list(WORK_CATEGORIES.keys())
    user_profile = Profile.objects.filter(user=request.user).values_list('likes', flat=True)
    context = {
        'user_profile': user_profile,
        'cvs': paged_cvs,
        'count': cvs.count(),
        'selected_speciality': selected_speciality,
        'selected_cities': selected_cities,
        'user': request.user,

    }
    return render(request, "all_cvs.html", context=context)


def list_cvs(request, page=1):
    cvs = CvForm.objects.all()
    paginator = Paginator(cvs, 20)
    page_number = request.GET.get('page', 1)
    try:
        cvs = paginator.page(page)
    except EmptyPage:
        cvs = paginator.page(paginator.num_pages)

    context = {
        'cvs': cvs,
        'page': page_number,

    }
    return render(request, 'cvs_all.html', context=context)


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
    cvs = CvForm.objects.all()
    selected_cities = list(CITY.keys())
    selected_speciality = list(WORK_CATEGORIES.keys())
    user_profile = Profile.objects.filter(user=request.user).values_list('likes', flat=True)
    context = {
        'user_profile': user_profile,
        'cvs': cvs,
        'count': cvs.count(),
        'selected_speciality': selected_speciality,
        'selected_cities': selected_cities,
        'user': request.user,

    }
    return render(request, 'all_cvs.html', context=context)


@login_required
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


@login_required
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
    try:
        profile = Profile.objects.get(user=request.user)
        cv_forms = profile.likes.all()
        context = {
            'cvs': cv_forms
        }
        return render(request, 'liked_cvs.html', context=context)
    except ObjectDoesNotExist:
        messages.warning(request, f"You do not have any liked CV")
        return render(request, 'all_cvs.html')
