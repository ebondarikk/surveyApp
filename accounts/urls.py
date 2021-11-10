from django.conf.urls import url

from . import views

urlpatterns = [
    url("login/", views.Login.as_view({"post": "login"}), name="accounts-login"),
    url("logout/", views.Logout.as_view(), name="accounts-logout"),
]
