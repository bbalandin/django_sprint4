"""blogicum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import (PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.conf import settings
from django.conf.urls.static import static
from users.forms import CreationForm


urlpatterns = [
    path('', include("blog.urls", namespace='blog')),
    path('pages/', include("pages.urls", namespace='pages')),
    path('posts/', include("blog.urls", namespace='blog')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CreationForm,  # наследовать форму от UserCreationForm
            success_url=reverse_lazy('blog:index'),    # blog:index
        ),
        name='registration',
    ),
    path('auth/', include('users.urls', namespace='users')),
    path('password-reset/', PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        success_url=reverse_lazy('password_reset_done')),
        name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')),
        name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
    path(
        'logout/',
        LogoutView.as_view(template_name='registration/logged_out.html'),
        name='logout',
    ),
    # path(
    #     'change_password/',
    #     LogoutView.as_view(template_name='registration/logged_out.html'),
    #     name='logout',
    # ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.internal_server_error'
