from django.conf.urls import url, include
from app import views 
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
  url(r'^$', views.login,  name='login'),
  url(r'^login/$', views.login, name='login'),
  url(r'^login$', views.login, name='login'),
  ]