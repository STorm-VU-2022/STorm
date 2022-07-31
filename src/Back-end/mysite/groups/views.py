from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect

from news.models import Publication
from users.models import Teacher
from .forms import CreateGroupForm
from .models import Methodic_group, Participates_in, Invites


@login_required
def group_creation(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()

            Participates_in.objects.create(
                member=Teacher.objects.get(pk=request.user.pk),
                group=Methodic_group.objects.get(pk=group.pk),
                is_accepted=True,
            )

            return redirect('profile-group', group.pk)
        else:
            return render(request, 'groups/group-creation.html', {'name_error': True, 'form': form})
    else:
        form = CreateGroupForm()
        return render(request, 'groups/group-creation.html', {'form': form})


def group_search(request):
    context = {}

    if request.method == 'POST':
        search_keywords = request.POST['search_keywords']
        groups = Methodic_group.objects.filter(name__icontains=search_keywords)
        context.update(
            {
                'groups': groups,
                'search_keywords': search_keywords,
            }
        )
    else:
        groups = Methodic_group.objects.all()
        context.update({'groups': groups, })

    return render(request, "groups/search-group.html", context=context)


def group_profile(request, group_pk):
    group_pk, group_creator = Methodic_group.objects.values_list('pk', 'creator').get(pk=group_pk)
    group = Methodic_group.objects.get(pk=group_pk)

    no_of_likes_from_related_publications = sum(list(Publication.objects.filter(related_to_group=group_pk).annotate(no_of_likes=Count('likes')).values_list('no_of_likes', flat=True)))

    group_participants = Participates_in.objects.filter(group=Methodic_group.objects.get(pk=group_pk))
    # print("In group " + str(group_participants.count()) + " members + followers")
    # print("In group " + str(group_participants.filter(is_accepted=True).count()) + " accepted members")
    # print("In group " + str(group_participants.filter(is_accepted=False).count()) + " followers")

    context = {
        'group_pk': group_pk,
        # 'no_of_group_members': group_participants.filter(is_accepted=True).count(),
        'no_of_group_members': group_participants.count(),  # Now it actually shows no of followers + members
        'group': group,
        'related_publications': Publication.objects.filter(related_to_group=group_pk).order_by('-likes'),
        'no_of_likes': no_of_likes_from_related_publications,
    }

    if group_creator == request.user.pk:
        context.update({
            'user_is_creator': True,
        })

    if Participates_in.objects.filter(member=request.user.pk, group=group_pk).exists():
        context.update({
            'is_user_follower': True,
        })

    return render(request, "groups/group-profile.html", context=context)


@login_required
def group_invite_user(request, user_pk):
    if request.user.pk == user_pk:
        return redirect('view-profile', request.user.pk)

    groups = Methodic_group.objects.filter(creator=request.user.pk)

    context = {
        'user': Teacher.objects.get(pk=user_pk),
        'groups': groups,
    }

    if request.method == 'POST':
        invited_to_group = Methodic_group.objects.get(name=request.POST.get('group_selection'))

        invites = Invites.objects.filter(invited_user=user_pk, group=invited_to_group)
        participations = Participates_in.objects.filter(member=user_pk, group=invited_to_group)

        if invites.exists() or participations.exists():
            # That means user is already invited to this group
            context.update({
                "already_invited_error": request.POST.get('group_selection'),
            })
            return render(request=request, template_name='groups/group-invite-user.html', context=context)

        if groups.filter(name=request.POST.get('group_selection')).exists():
            Invites.objects.create(
                invited_user=Teacher.objects.get(pk=user_pk),
                group=invited_to_group
            )
            context.update({
                'success_message': "You successfully invited " + str(Teacher.objects.get(pk=user_pk)) + " to group \"" + str(invited_to_group) + "\"",
                'group': invited_to_group,
            })
        else:
            context.update({
                "error_message": request.POST.get('group_selection'),
            })

    return render(request=request, template_name='groups/group-invite-user.html', context=context)


@login_required
def my_groups(request):
    groups_ids = Participates_in.objects.filter(member=request.user.pk).order_by('-is_accepted', 'group').values_list('group_id', flat=True)
    following_groups = Methodic_group.objects.filter(pk__in=groups_ids).values('pk', 'name')
    invites = Invites.objects.filter(invited_user=request.user.pk).order_by('-invitation_date').all()

    context = {
        'following_groups': following_groups,
        'invites': invites,
    }
    return render(request, "groups/my-groups.html", context=context)


@login_required
def group_edit(request):
    return render(request, "groups/group-edit.html")


@login_required
def group_follow(request, group_pk):
    Participates_in.objects.create(
        member=Teacher.objects.get(pk=request.user.pk),
        group=Methodic_group.objects.get(pk=group_pk),
    )
    return redirect('profile-group', group_pk)


@login_required
def group_unfollow(request, group_pk, do_redirect_to_group=False):
    if request.method == 'POST':
        groups_following = Participates_in.objects.filter(group=group_pk, member=request.user.pk).all()
        groups_following.delete()
        if do_redirect_to_group:
            return redirect('profile-group', group_pk)
    return redirect('my-groups')


@login_required
def group_invitation_accept(request, invitation_pk):
    if request.method == 'POST':
        invitation = Invites.objects.get(pk=invitation_pk)

        Participates_in.objects.create(
            member=Teacher.objects.get(pk=request.user.pk),
            group=Methodic_group.objects.get(pk=invitation.group.pk),
            is_accepted=True
        )

        invitation.delete()

    return redirect('my-groups')


@login_required
def group_invitation_reject(request, invitation_pk):
    if request.method == 'POST':
        Invites.objects.get(pk=invitation_pk).delete()
    return redirect('my-groups')


@login_required
def group_invitation_accept(request, invitation_pk):
    if request.method == 'POST':
        invitation = Invites.objects.get(pk=invitation_pk)

        Participates_in.objects.create(
            member=Teacher.objects.get(pk=request.user.pk),
            group=Methodic_group.objects.get(pk=invitation.group.pk),
            is_accepted=True
        )

        invitation.delete()

    return redirect('my-groups')
