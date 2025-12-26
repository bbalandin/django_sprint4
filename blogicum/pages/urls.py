from django.urls import path

from . import views


app_name = 'pages'
urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
    path('rules/', views.RulesView.as_view(), name='rules'),

]
handler404 = 'pages.views.page_not_found'
handler403 = 'pages.views.csrf_failure'
handler500 = 'pages.views.server_error'
