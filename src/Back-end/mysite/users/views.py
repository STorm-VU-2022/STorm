from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from news.models import Publication
from .forms import EditProfileForm, RecommendationForm
from .forms import SignUpForm
from .models import Teacher


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            return redirect('/users/login')
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})


def index(request):
    return HttpResponse("Hi, we know that you should not be able to see this page, but we call this an 'Easter Egg'</br>"
                        "To change this, go to module 'users' -> views.py -> index and change return (uncomment)")
    # return redirect('browse-publications')


def profile(request):
    # return render(request, 'users/profile.html')  # <-- This one is broken, as I can see, this is still being used after authentication
    return redirect('view-profile', request.user.pk)


@login_required
def edit(request):
    user_information = {
        'self_description': request.user.self_description,
        'profile_picture': request.user.profile_picture,
        'profession': request.user.profession,
        'facebook_link': request.user.facebook_link,
        'twitter_link': request.user.twitter_link,
        'instagram_link': request.user.instagram_link,
        'linkedin_link': request.user.linkedin_link,
    }
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if ("https://www.facebook.com/" in request.user.facebook_link or request.user.facebook_link=="") and ("https://twitter.com/" in request.user.twitter_link or request.user.twitter_link=="") and ("https://twitter.com/" in request.user.twitter_link or request.user.twitter_link=="") and ("https://www.linkedin.com/in/" in request.user.linkedin_link or request.user.linkedin_link==""):
                form.save()
                return redirect('view-profile', request.user.pk)     
            else:
                return render(request, 'users/profile_edit.html', {'name_error': True, 'form': form})
        else:
            return render(request, 'users/profile_edit.html', {'name_error': True, 'form': form})
    else:
        form = EditProfileForm(initial=user_information)
    return render(request, 'users/profile_edit.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'users/login.html')


def convert_teacher_to_dictionary(teacher):
    teacher_dict = {
        "teacher_pk": teacher.pk,
        "name": teacher.full_name,
        "email": teacher.email,
        "profile_picture": teacher.profile_picture,
        "self_description": teacher.self_description,
        "profession": teacher.profession,
    }

    total_publication_likes = 0
    for publication in Publication.objects.filter(creator_id=teacher.pk):
        total_publication_likes += publication.likes.through.objects.filter(publication_id=publication.pk).count()

    teacher_dict.update({"total_publication_likes": total_publication_likes, })
    return teacher_dict


@login_required
def leaderboard(request):
    list_of_teachers = []
    for teacher in Teacher.objects.all():
        list_of_teachers.append(convert_teacher_to_dictionary(teacher))
    list_of_teachers = sorted(list_of_teachers, key=lambda i: i['total_publication_likes'], reverse=True)

    context = {
        "teachers": list_of_teachers,
    }

    paginator = Paginator(list_of_teachers, 20)  # Show 20 users per page.
    page_number = request.GET.get('page')
    teachers = paginator.get_page(page_number)

    return render(request, 'users/leaderboard.html', {'teachers': teachers})


@login_required
def user_search(request):
    if request.method == 'POST':
        search_keywords = request.POST['search_keywords']
        obj_list = Teacher.objects.all().filter(full_name__icontains=search_keywords)
        paginator = Paginator(obj_list, 12)  # Show 12 users per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "users/search-user.html", {'page_obj': page_obj})
    else:
        obj_list = Teacher.objects.all()
        paginator = Paginator(obj_list, 12)  # Show 12 users per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "users/search-user.html", {'page_obj': page_obj})


@login_required
def add_profile_recommendation(request, profile_pk):
    """
        ID of user who wrote recommendation:   request.user.pk
        ID of user who received recommendation: profile_pk

        = = = How it works? = = =
        Django model form is used to generate TextField for writing a recommendation
        Variable 'is_self_profile' is used to check if user have opened his/her profile and, if needed, hide
            the form needed for writing recommendation.

        = = = What can be improved? = = =
        Good question, I do not know at the moment (May 30, 2022)
    """
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        recommendation = form.save(commit=False)
        recommendation.recommender = Teacher.objects.get(pk=request.user.pk)
        recommendation.recommended = Teacher.objects.get(pk=profile_pk)
        if form.is_valid():
            form.save()
            print(f'NEW RECOMMENDATION: UserID {profile_pk} just received a recommendation from userID {request.user.pk}!')

    return redirect('view-profile', profile_pk)
