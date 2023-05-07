from django.urls import path
from . import views

app_name = "login"   


urlpatterns = [
    #path("", views.homepage, name="homepage"),
    path("", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path("homepage/", views.homepage, name= "homepage"),
]