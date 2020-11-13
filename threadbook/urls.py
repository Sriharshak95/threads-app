"""threadapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url
from django.contrib import admin
# from tastypie.api import Api

#from threadbook.api import UserResource, UserSocialAuthResource
from threadbook.views import index, signin, signup, logout, home, profile

from threadbook.searchbooks import search

# from threadapp.twitterapp import twitter_login, twitter_logout, twitter_authenticated

import threadcard

from threadcard import views
from django.views.static import serve

admin.autodiscover()

#v1_api = Api(api_name='v1')
#v1_api.register(UserResource())
#v1_api.register(UserSocialAuthResource())

urlpatterns = patterns('',
    # Examples:
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^$', index, name='index'),

    # ---- for podcast ----------------- 
    url(r'^podcast/$', views.podcast, name='podcast'),
    url(r'^(?P<username>\w+)/podcast/(?P<pk>\w+)/$', views.podcastbook, name='podcastbook'),
    url(r'^podcastlist/(?P<pk>\w+)/$', views.podcastlist, name='podcastlist'),

    # url(r'^sendemail/', views.sendemail, name='sendemail'),
    url(r'^sendemail/(?P<pk>\w+)/', views.sendemail, name='sendemail'),

    # url(r'^login/?$', twitter_login),
    # url(r'^logout/?$', twitter_logout),
    # url(r'^authenticated/?$', twitter_authenticated),

    url(r'^signin', signin, name='signin'),
    url(r'^signup', signup, name='signup'),
    url(r'^logout', logout, name='logout'),
    # url(r'^home', home, name='home'),
    url(r'^profile$', profile, name='profile'),
    # url(r'^accounts/profile', profile, name='profile'),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^oauth/', name='127.0.0.1/oauth/complete/twitter/'),
    url(r'^adminlogin/', views.adminlogin, name='adminlogin'),

    url(r'^(.*)/home/$', home, name='home'),

    url(r'^(.*)/createlist/$', views.create_thread, name='create_thread'),
    # url(r'^(.*)/list/$', views.list_thread, name='list_thread'),
    url(r'^(.*)/list/$', views.list, name='list'),
    url(r'^(.*)/books/$', views.books, name='books'),

    url(r'^projection/$', views.projection, name='projection'),
    url(r'^createpodcast/$', views.createpodcast, name='createpodcast'),
    url(r'^podcastpool/$', views.podcastpool, name='podcastpool'),
    url(r'^podcastshare/$', views.podcastshare, name='podcastshare'),
    # url(r'^(.*)/(.*)/card/(?P<pk>[0-9]+)/$', views.edit_thread, name='edit_thread'),

    url(r'^(?P<username>\w+)/(?P<pk>\w+)/$', views.edit_thread, name='edit_thread'),
    
    url(r'^adminpage/$', views.adminpage, name='adminpage'),


    # url(r'^$', 'django_social_app.views.login'),

    #(r'^api/', include(v1_api.urls)),
    url(r'^api/searchbooks/(?P<user_input>\w+)/$', search, name='search'),

    url(r'^threadcard/', include('threadcard.urls')),

)


if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += patterns('',url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = threadcard.views.handler404

handler500 = threadcard.views.handler500
