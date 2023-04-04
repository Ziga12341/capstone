from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Group, Category, Categorised_list, Suggestions, Comment


# Create new group form
class NewGroupForm(forms.Form):
    group_name = forms.CharField(label="Group name", max_length=64)
    group_description = forms.CharField(label="Group description", max_length=256)
    # group_image = forms.URLField(label="Group image", required=False)


def index(request):
    return render(request, "votingapp/index.html")


@login_required
def groups(request):
    """
    get user from request like user id
    user can create new group
    :param request:
    :return:
    """
    user = User.objects.get(id=request.user.id)
    my_groups = Group.objects.filter(members=user)
    if request.method == "POST":
        form = NewGroupForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data["group_name"]
            group_description = form.cleaned_data["group_description"]
            # group_image = form.cleaned_data["group_image"]
            new_group = Group(group_name=group_name, group_description=group_description, owner=user)
            new_group.save()
            new_group.members.add(user)
            return HttpResponseRedirect(reverse("groups"))
        else:
            return render(request, "votingapp/groups.html", {
                "my_groups": my_groups,
                "user": user,
                "form": NewGroupForm()
            })
    return render(request, "votingapp/groups.html", {
        "my_groups": my_groups,
        "user": user,
        "form": NewGroupForm()
    })


def login_view(request):
    """
    Log user in.
    :param request:
    :return:
    """
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "votingapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "votingapp/login.html")


def logout_view(request):
    """
    Log user out.
    :param request:
    :return:
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    Register user.
    :param request:
    :return:
    """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "votingapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "votingapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "votingapp/register.html")
