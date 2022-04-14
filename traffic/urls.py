from django.urls import path
from . import views

app_name = 'traffic'
urlpatterns=[
    path('',views.home, name='home'),
    path('list/',views.homeListAPIView.as_view(), name='list'),
]