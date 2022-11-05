"""pitch_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, register_converter
from datetime import datetime

from pitch_management.views import (add_pitch_request, delete_pitch_request,
                                    edit_pitch_request, homepage,
                                    login_request, logout_request,
                                    manage_pitch_table, password_reset_request,
                                    register_request, view_pitch_table, book_pitch, my_booking,
                                    delete_booking_request)

class DateConverter:
    regex = '\d{4}-\d{1,2}-\d{1,2}'
    format = '%Y-%m-%d'

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)

register_converter(DateConverter, 'date')

urlpatterns = [
    path("", homepage, name="homepage"),
    path("admin/", admin.site.urls),
    path("register/", register_request, name="register"),
    path("add_pitch/", add_pitch_request, name="add_pitch"),
    path("manage_pitch/", manage_pitch_table, name="manage_pitch"),
    path("edit_pitch/<slug:uidb64>", edit_pitch_request, name="edit_pitch"),
    path("delete_pitch/<slug:uidb64>", delete_pitch_request, name="delete_pitch"),
    path("view_pitch/", view_pitch_table, name="view_pitch"),
    path("book_pitch/<date:date>/<slug:uidb64>", book_pitch, name="book_pitch"),
    path("my_booking", my_booking, name="my_booking"),
     path("delete_booking/<slug:uidb64>", delete_booking_request, name="delete_booking"),
    path("login/", login_request, name="login"),
    path("reset_pass/", password_reset_request, name="password_reset_request"),
    path(
        "reset_pass/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("logout", logout_request, name="logout"),
]
