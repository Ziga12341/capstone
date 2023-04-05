from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("groups", views.groups, name="groups"),
    path("group/<str:group_name>", views.group, name="group"),
    path("group/<str:group_name>/<str:category_name>", views.category, name="category"),
    path("group/<str:group_name>/<str:category_name>/<str:suggestion_name>", views.suggestion, name="suggestion"),
]
