from . import views
from django.urls import path, reverse_lazy
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)


app_name = 'users'
urlpatterns = [
    path(
        'logout/',
        LogoutView.as_view(template_name='registration/logged_out.html'),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            success_url=reverse_lazy('users:password_reset_done')),
        name='password_reset_form'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete')),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]
