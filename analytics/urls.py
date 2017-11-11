from django.conf.urls import url
from . import views

app_name = 'analytics'

urlpatterns = [
        url(r'^file_upload$', views.file_upload, name='file_upload'),
        url(r'^uploaded$', views.uploaded, name='uploaded'),
        url(r'^index$', views.index, name='index'),
    ]
