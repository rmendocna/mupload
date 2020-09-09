from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('dl/<hash>/', fetch, name='fetch')
]
