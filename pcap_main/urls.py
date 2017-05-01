from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'read/?$', views.read, name="read"),
    url(r'read/(?P<filename>.+)', views.readfile, name="readfile")
]
