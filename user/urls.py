from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard/', views.penel, name='person panel'),
    path('verify/', views.verify, name='personVerify'),
    path('ballot/vote', views.show_sheet, name='show_sheet'),
    path('ballot/vote/preview', views.preview_score, name='preview_score'),
    path('ballot/vote/submit', views.submit_sheet, name='submit_sheet'),
]
