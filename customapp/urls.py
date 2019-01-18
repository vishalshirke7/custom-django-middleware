from django.urls import path

from . import views


urlpatterns = [
    path('login', views.login, name='login'),
    path('test_api/', views.testapi, name='testapi'),

]

