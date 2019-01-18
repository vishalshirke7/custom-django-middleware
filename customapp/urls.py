from django.urls import path

from . import views

app_name = 'customapp'


urlpatterns = [
    path('login', views.login, name='login'),
    path('test_api/', views.testapi, name='testapi'),

]

