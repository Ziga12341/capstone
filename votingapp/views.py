from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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


# Create new category in particular categorised list form
class NewCategoryForm(forms.Form):
    category_name = forms.CharField(label="Category name", max_length=64)


def index(request):
    return render(request, "votingapp/index.html")


@login_required
def groups(request):
    """
    get user from request like user id
    user can create new group
    when you create new group you are automatically owner of this group as well as member
    when you create new group you get a default categorised list with no categories in it
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
            default_categorised_list = Categorised_list(group=new_group, category=None)
            default_categorised_list.save()
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


# user need to be member of group to see group page
# detailed view of particular group
# user can create categorised list of this group
# add category to categorised list of group
@login_required
def group(request, group_id):
    """
    get group from request like group id
    user see a default categorised list with categories in it
    :param request:
    :param group_id:
    :return:
    """
    group_by_id = Group.objects.get(id=group_id)
    user = User.objects.get(id=request.user.id)
    default_categorised_lists = Categorised_list.objects.get(group=group_by_id)
    print("----------- group", default_categorised_lists.group)
    print("----------- category", default_categorised_lists.category)
    categories = default_categorised_lists.category
    # if there is any category in this categorised list
    if user not in group_by_id.members.all():
        return JsonResponse({"error": "You can view detailed view of group which you are a member."},
                            status=400)

    if request.method == "POST":
        category_name = request.POST["category_name"]
        category = Category.objects.get(category_name=category_name)
        new_categorised_list = Categorised_list(group=group_by_id, category=category)
        new_categorised_list.save()
        return HttpResponseRedirect(reverse("group", args=(group_by_id.id,)))

    return render(request, "votingapp/group.html", {
        "group": group_by_id,
        "user": user,
        "categories": categories,
        "form": NewCategoryForm()
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
