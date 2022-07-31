from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render, redirect

from users.forms import RecommendationForm
from users.models import Teacher, Recommends
from groups.models import Methodic_group, Participates_in
from .forms import UploadFileForm, CommentPublicationForm
from .models import Publication, Subject, Downloads, Comments


def homepage(request):
    list_of_teacher_pks = list(Teacher.objects.values_list('pk', flat=True))

    list_teacher_pk_and_total_no_of_likes = []
    for pk in list_of_teacher_pks:
        total_no_of_likes = Publication.objects.filter(creator_id=pk).values('likes').count()
        list_teacher_pk_and_total_no_of_likes.append([pk, total_no_of_likes])

    list_teacher_pk_and_total_no_of_likes.sort(key=lambda x: x[1], reverse=True)  # Sorts list by total no of likes
    list_teacher_pk_and_total_no_of_likes = list_teacher_pk_and_total_no_of_likes[:3]       # Leave top 3 results

    # Get PKs of top 3 teachers
    get_PKs = lambda: [x[0] for x in list_teacher_pk_and_total_no_of_likes]
    pks_of_top_teachers = get_PKs()

    # Get top teachers
    teacher_dictionaries = list(Teacher.objects.filter(pk__in=pks_of_top_teachers).values('pk', 'profile_picture', 'full_name', 'profession', 'self_description', ))

    # = = = Get top publications = = =
    publication_pks = list(Publication.objects.values_list('pk', flat=True))

    list_publication_pk_and_total_no_of_likes = []
    for pk in publication_pks:
        publication_likes = Publication.objects.get(pk=pk).likes.count()
        list_publication_pk_and_total_no_of_likes.append([pk, publication_likes])

    list_publication_pk_and_total_no_of_likes.sort(key=lambda x: x[1], reverse=True)  # Sorts list by no of likes
    list_publication_pk_and_total_no_of_likes = list_publication_pk_and_total_no_of_likes[:3]       # Leave top 3 results

    publication_dictionaries = []

    for pk, no_of_likes in list_publication_pk_and_total_no_of_likes:
        publication = Publication.objects.filter(pk=pk).values('pk', 'photo', 'creator_id', 'title', 'subject', 'student_year', 'language', 'short_description')
        publication = publication[0]
        author = Teacher.objects.get(pk=publication.get('creator_id')).full_name
        subject_name = Subject.objects.get(pk=publication.get('subject')).name
        publication.update({
            'author': author,
            'subject': subject_name,
            'likes': no_of_likes,
        })
        publication_dictionaries.append(publication)

    context = {
        'teachers': teacher_dictionaries,
        'publications': publication_dictionaries,
    }

    return render(request, "news/homepage.html", context=context)


@login_required
def material_info(request):
    return render(request, "news/material.html")


def convert_publication_to_dictionary(pub):
    publication_dictionary = {
        "pk": pub.pk,
        "photo": pub.photo,
        "author_name": pub.creator_id.full_name,
        "author_pk": pub.creator_id.pk,
        "title": pub.title,
        "subject": pub.subject.name,
        "student_year": pub.student_year,
        "language": pub.language,
        "short_description": pub.short_description,
        "likes": pub.likes.count(),
    }
    return publication_dictionary


def get_dictionary_of_subjects(selected_subject=None):
    # TODO: review possibility of retrieving only subjects which have associated publications
    #   to do that - take a look how languages are retrieved in get_dictionary_of_languages()
    subject_list = list(Subject.objects.values_list('name', flat=True).order_by('name'))
    subject_dictionaries = []

    for subject in subject_list:
        subject_dictionaries.append({
            'name': subject,
            'is_selected': False,
        })
    if selected_subject:    # If subject is selected, set its selection in HTML as active
        selected_subject_index = subject_list.index(selected_subject)
        subject_to_set_selection = subject_dictionaries[selected_subject_index]
        subject_to_set_selection.update({'is_selected': True, })
        subject_dictionaries[selected_subject_index] = subject_to_set_selection

    return subject_dictionaries


def get_dictionary_of_languages(selected_language=None):
    languages = list(Publication.objects.values_list('language', flat=True).order_by('language').distinct())
    language_dictionaries = []

    for language in languages:
        language_dictionaries.append({
            'name': language,
            'is_selected': False,
        })
    if selected_language:
        selected_language_index = languages.index(selected_language)
        language_to_set_selection = language_dictionaries[selected_language_index]
        language_to_set_selection.update({'is_selected': True, })
        language_dictionaries[selected_language_index] = language_to_set_selection

    return language_dictionaries


def get_dictionary_of_grades(selected_grade=None):
    grades = list(Publication.objects.values_list('student_year', flat=True).order_by('student_year').distinct())
    grade_dictionaries = []

    for grade in grades:
        grade_dictionaries.append({
            'name': grade,
            'is_selected': False,
        })
    if selected_grade:
        selected_grade = int(selected_grade)
        selected_grade_index = grades.index(selected_grade)
        grade_to_set_selection = grade_dictionaries[selected_grade_index]
        grade_to_set_selection.update({'is_selected': True, })
        grade_dictionaries[selected_grade_index] = grade_to_set_selection

    return grade_dictionaries


def search(request):
    sort_options = [
        {'name': 'Alphabetically A-Z', 'selected': False},
        {'name': 'Alphabetically Z-A', 'selected': False},
        {'name': 'Newest First', 'selected': False},
        {'name': 'Oldest First', 'selected': False},
        {'name': 'Likes', 'selected': False},
    ]

    if request.method == 'POST':
        search_keywords = request.POST['search_keywords']
        search_sort = request.POST['search_sort']
        search_subject = request.POST.get('search_subject')
        search_grade = request.POST.get('search_grade')
        search_language = request.POST.get('search_language')
        search_group = request.POST.get('search_group')

        # print('\n\n|+| Your searched something with POST:', search_keywords,
        #       '\n|+| Sort by:', search_sort,
        #       '\n|+| Filters:', search_subject, search_grade, search_language, search_group,
        #       '\n\n')
        publications_objects = Publication.objects.filter(title__icontains=search_keywords)

        subjects = get_dictionary_of_subjects(selected_subject=search_subject)
        languages = get_dictionary_of_languages(selected_language=search_language)
        grades = get_dictionary_of_grades(selected_grade=search_grade)

        # Applying sorting
        if search_sort == 'Alphabetically A-Z':
            publications_objects = publications_objects.order_by('title')
            sort_options[0] = {'name': 'Alphabetically A-Z', 'selected': True}

        if search_sort == 'Alphabetically Z-A':
            publications_objects = publications_objects.order_by('-title')
            sort_options[1] = {'name': 'Alphabetically Z-A', 'selected': True}

        if search_sort == 'Newest First':
            publications_objects = publications_objects.order_by('-created_at')
            sort_options[2] = {'name': 'Newest First', 'selected': True}

        if search_sort == 'Oldest First':
            publications_objects = publications_objects.order_by('created_at')
            sort_options[3] = {'name': 'Oldest First', 'selected': True}

        if search_sort == 'Likes':
            publications_objects = publications_objects.order_by('-likes')
            sort_options[4] = {'name': 'Likes', 'selected': True}

        # Filtering by subject
        if search_subject:
            search_subject = Subject.objects.get(name=search_subject)
            publications_objects = publications_objects.filter(subject=search_subject)

        # Filtering by grade
        if search_grade:
            publications_objects = publications_objects.filter(student_year=search_grade)

        # Filtering based on language
        if search_language:
            publications_objects = publications_objects.filter(language=search_language)

        # Filtering based on group
        if search_group:
            publications_objects = publications_objects.filter(related_to_group=Methodic_group.objects.get(pk=int(search_group)))

        publications_list = []
        for pub in publications_objects:
            publications_list.append(convert_publication_to_dictionary(pub))

        paginator = Paginator(publications_list, 10000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)




    else:
        publications_objects = Publication.objects.all()
        subjects = get_dictionary_of_subjects()
        languages = get_dictionary_of_languages()
        grades = get_dictionary_of_grades()

        publications_list = []
        for pub in publications_objects:
            publications_list.append(convert_publication_to_dictionary(pub))

        paginator = Paginator(publications_list, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


    pks_of_groups_with_publications = Publication.objects.exclude(related_to_group=None).values_list('related_to_group', flat=True)
    pks_of_groups_with_publications = list(dict.fromkeys(pks_of_groups_with_publications))

    context = {
        "publications": page_obj,
        'grades': grades,
        'languages': languages,
        'sort_options': sort_options,
        'subjects': subjects,
        'groups': Methodic_group.objects.filter(pk__in=pks_of_groups_with_publications),
    }

    return render(request, "news/search.html", context=context)


@login_required
def material_upload(request):
    context = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.creator_id = request.user
            material.save()
            return HttpResponseRedirect('/news/search/')
        else:
            return render(request, 'news/upload.html', {'form': form, 'error': True},)
    else:
        pks_of_available_groups = list(Participates_in.objects.filter(is_accepted=True, member=request.user.pk).values_list('group', flat=True))
        available_groups = Methodic_group.objects.filter(pk__in=pks_of_available_groups)
        context.update({'available_groups': available_groups, })
        form = UploadFileForm()
    context.update({'form': form})
    return render(request, 'news/upload.html', context=context)


def view_publication(request, publication_pk):
    publication = Publication.objects.get(id=publication_pk)

    if request.method == 'POST':
        form = CommentPublicationForm(request.POST)
        commentary = form.save(commit=False)
        commentary.teacher = request.user
        commentary.publication = publication

        if form.is_valid():
            commentary.save()
            return redirect('view-publication', publication_pk)

    context = {
        'publication': publication,
        'likes': publication.likes.count(),
        'commentaries': Comments.objects.filter(publication=publication).all().order_by('-comment_date'),
        'form': CommentPublicationForm(),
    }

    return render(request, "news/material.html", context=context)


def get_recommendations(teacher_pk):
    recommendations = Recommends.objects.filter(recommended=teacher_pk)
    list_of_recommendations = []

    for recommendation in recommendations:
        list_of_recommendations.append(
            {
                'author': recommendation.recommender.full_name,
                'text': recommendation.recommendation_text,
            }
        )

    return list_of_recommendations


def get_top_publications(list_publication_pk_and_no_of_likes):
    publications_list = []
    pks_of_top_rated_publications = []

    list_publication_pk_and_no_of_likes.sort(key=lambda x: x[1], reverse=True)  # Sorts list of publication by their popularity

    for i in range(len(list_publication_pk_and_no_of_likes)):
        pks_of_top_rated_publications.append(list_publication_pk_and_no_of_likes[i][0])
        if i == 2:  # As the list of publication_pks and no_of_likes is already sorted, we only need max first 3 publications
            break

    if len(pks_of_top_rated_publications) == 1:
        top_publications_objects = Publication.objects.get(pk=pks_of_top_rated_publications[0])
        publications_list.append(convert_publication_to_dictionary(top_publications_objects))

    if len(pks_of_top_rated_publications) == 2:
        top_publications_objects = Publication.objects.filter(
            Q(pk=pks_of_top_rated_publications[0]) | Q(pk=pks_of_top_rated_publications[1]))
        for pub in top_publications_objects:
            publications_list.append(convert_publication_to_dictionary(pub))

    if len(pks_of_top_rated_publications) == 3:
        top_publications_objects = Publication.objects.filter(
            Q(pk=pks_of_top_rated_publications[0]) | Q(pk=pks_of_top_rated_publications[1]) | Q(
                pk=pks_of_top_rated_publications[2]))
        for pub in top_publications_objects:
            publications_list.append(convert_publication_to_dictionary(pub))

    return publications_list


def view_user(request, teacher_pk):
    teacher = Teacher.objects.get(id=teacher_pk)

    publication_pks = Publication.objects.filter(creator_id=teacher_pk).values_list('pk', flat=True)
    no_of_publication_downloads = Downloads.objects.filter(publication__in=publication_pks).count()
    no_of_followers = Teacher.follows.through.objects.filter(to_teacher=teacher_pk).count()
    publications = Publication.objects.filter(creator_id=teacher_pk)

    summary_likes = 0
    list_publication_pk_and_no_of_likes = []
    for pub in publications:  # TODO: review possibility of using iterators for performance boost
        publication_likes = pub.likes.through.objects.filter(publication_id=pub.pk).count()

        list_publication_pk_and_no_of_likes.append([pub.pk, publication_likes])
        summary_likes += publication_likes

    context = {
        'profile_pk': teacher.pk,
        'profile_picture': teacher.profile_picture,
        'profession': teacher.profession,
        'full_name': teacher.full_name,
        'self_description': teacher.self_description,
        'uploads': len(publications),
        'downloads': no_of_publication_downloads,
        'likes': summary_likes,
        'no_of_followers': no_of_followers,
        'publications': get_top_publications(list_publication_pk_and_no_of_likes),
        # Social media links:
        'facebook_link': teacher.facebook_link,
        'twitter_link': teacher.twitter_link,
        'instagram_link': teacher.instagram_link,
        'linkedin_link': teacher.linkedin_link,
        # Recommendations:
        'recommendations': get_recommendations(teacher_pk),
        'user': teacher,
    }

    if teacher_pk == request.user.pk:
        context.update({"is_self_profile": True, })
    else:
        form = RecommendationForm()
        context.update({'form': form, })

    return render(request, "users/profile.html", context=context)


def like_publication(request, publication_pk):
    """
        PK of liked publication:    publication_pk
        PK of user who liked the publication:   request.user.pk

        = = = How it works? = = =
        1. Checks if user is logged in
            case 'User IS logged in':
                Step 1: Get liked publication
                Step 2: Get user who liked the publication
                Step 3: Add to liked publication user who liked the publication and save changes

                NOTE: Steps 2 and 3 are performed in a single line

            case 'User IS NOT logged in':
                Step 1: Do nothing

        2. User is redirected back to the publication


        = = = What can be improved? = = =
        1. Implement removing likes from liked publications
        2. Display like button in liked publication displaying differently from not-yet-liked publication
    """

    if request.user.pk:
        publication = Publication.objects.get(pk=publication_pk)
        publication.likes.add(Teacher.objects.get(pk=request.user.pk))
        print(datetime.now(), ": User ID", request.user.pk, 'liked publication ID', publication_pk)

    return redirect('view-publication', publication_pk)


def download_publication_materials(request, publication_pk):
    publication = Publication.objects.get(pk=publication_pk)

    if publication.media.url:
        material_name = str(publication.media).split('/')
        material_name = material_name[-1]
        if request.user.pk:
            print(datetime.now(), ": User ID", request.user.pk, 'downloaded materials from publication ID',
                  publication_pk)
            # publication.downloads.add(Teacher.objects.get(pk=request.user.pk))    # Can be used for unique downloads
            Downloads.objects.create(publication=publication, teacher=Teacher.objects.get(pk=request.user.pk))
        else:
            anonymous_user, is_created_right_now = Teacher.objects.get_or_create(
                username='anonymous user',
                full_name='anonymous user who is used to track downloads by unauthorised users',
                email='ohboynowaysomeonehasthesamemail@storm.com',
                profession='Anonymus',
            )
            print(datetime.now(), ": User ID", anonymous_user.pk, '(anonymous user) downloaded materials from publication ID',
                  publication_pk)

            if is_created_right_now:
                print(datetime.now(), ": We have our first anonymous download! ID used for anonymous users is",
                      anonymous_user.pk)
            # publication.downloads.add(Teacher.objects.get(pk=anonymous_user.pk))        # Can be used for unique downloads
            Downloads.objects.create(publication=publication, teacher=Teacher.objects.get(pk=anonymous_user.pk))

        return FileResponse(open(publication.media.path, 'rb'), as_attachment=True)

        # return redirect(publication.media.url)
    # This final redirect simply redirects back to publication if someone somehow managed to get to this endpoint and
    #   tries to download not existing publication materials
    return redirect('view-publication', publication_pk)
