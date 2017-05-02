from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'read/?$', views.read, name="read"),
    url(r'read/(?P<filename>.+)', views.readfile, name="readfile"),
    url(r'settings/edit', views.settings_page_edit, name="settings_page_edit"),
    url(r'settings/', views.settings_page, name="settings_page"),
    url(r'$', views.home, name="home")
]
