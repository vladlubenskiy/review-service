from django.conf.urls import patterns, include, url

from review_service.oauth.google.authentication import urls as authentication_urls
from services import views

urlpatterns = patterns('',
    url(r'^$', views.MainPage), # page only for users
    url(r'^auth/', include(authentication_urls)),
)
