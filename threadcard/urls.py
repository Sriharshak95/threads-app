__author__ = 'leif'

from django.conf.urls import patterns, url
from threadcard import views
from . import api_views
from . import api

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),

        url(r'^api/listuser/$', api_views.UserList.as_view()),
        url(r'^api/addcategory/$', api_views.AddCategory.as_view()),
        url(r'^api/listcategory/$', api_views.AddCategory.as_view()),
        url(r'^api/editcategory/(?P<pk>[0-9]+)/$', api_views.EditCategory.as_view()),

        url(r'^api/addbookcover/$', api_views.AddBookcover.as_view()),
        url(r'^api/listbookcover/$', api_views.ListBookcover.as_view()),
        url(r'^api/editbookcover/(?P<pk>\w+)/$', api_views.EditBookcover.as_view()),

        url(r'^api/addthread/$', api_views.AddThread.as_view()),
        url(r'^api/listthread/(?P<bookcover>\w+)/$', api_views.ListThread.as_view()),
        url(r'^api/editthread/(?P<pk>[0-9]+)/$', api_views.EditThread.as_view()),


        url(r'^api/addsubcomment/$', api_views.AddSubComment.as_view()),
        url(r'^api/listsubcomment/(?P<threadid>[0-9]+)/$', api_views.ListSubComment.as_view()),
        url(r'^api/editsubcomment/(?P<pk>[0-9]+)/$', api_views.EditSubComment.as_view()),

        url(r'^listsubcomment/(?P<threadid>[0-9]+)/$', views.subcommentsList, name='subcommentsList'),

        url(r'^api/createthread/$', api.ThreadList.as_view()),

        url(r'^cats/(?P<catid>\w+)/$', views.category_show, name='cat'),

        url(r'^createcard/$', views.create_thread, name='create_thread'),
        url(r'^listcard/$', views.list_thread, name='list_thread'),
        url(r'^editcard/(?P<pk>[0-9]+)/$', views.edit_thread, name='edit_thread'),

        url(r'^api/deletebookcover/(?P<pk>\w+)/$', api_views.DeleteBookcover.as_view()),
        url(r'^api/deletethread/(?P<pk>[0-9]+)/$', api_views.DeleteThread.as_view()),
        url(r'^api/deletesubcomment/(?P<pk>[0-9]+)/$', api_views.DeleteSubComment.as_view()),

        #  FOR Like and Unlike Thread  call this url as api with argument (id of Bookcover) in url

        url(r'^likethread/(?P<pk>\w+)/$', views.like_thread, name='like_thread'),
        url(r'^unlikethread/(?P<pk>\w+)/$', views.unlike_thread, name='unlike_thread'),
        
        # for Comment to Whole thread (bookcover)
        url(r'^api/addrating/$', api_views.AddRating.as_view()),
        url(r'^api/listrating/(?P<pk>\w+)/$', api_views.ListRating.as_view()),
        url(r'^api/editrating/(?P<pk>[0-9]+)/$', api_views.EditRating.as_view()),

        url(r'^threadList/$', views.threadList, name='threadList'),
        url(r'^allthreadList/$', views.allthreadList, name='allthreadList'),
        url(r'^perticularthreadList/(?P<userid>[0-9]+)/$', views.perticularthreadList, name='perticularthreadList'),
        url(r'^podcastthreadList/(?P<userid>[0-9]+)/$', views.podcastthreadList, name='podcastthreadList'),

# for Subscribe thread 
        url(r'^api/subscribe/$', api_views.AddSubscribe.as_view()),
        # url(r'^api/editsubscribe/(?P<pk>[0-9]+)/$', api_views.EditSubscribe.as_view()),
        url(r'^api/unsubscribe/(?P<pk>[0-9]+)/$', api_views.UnSubscribe.as_view()),
        # url(r'^api/writtersubscribe/(?P<reader>[0-9]+)/$', api_views.ListSubscribefor.as_view()),
        url(r'^api/checksubscribe/(?P<from>[0-9]+)/(?P<to>[0-9]+)/$', api_views.CheckSubscribe.as_view()),

        url(r'^api/listsubscribers/(?P<userid>[0-9]+)/$', views.listsubscribers, name='listsubscribers'),

        url(r'^api/subscribedlist/(?P<userid>[0-9]+)/$', views.subscribedlist, name='subscribedlist'),
# Feedback 
        url(r'^api/addfeedback/$', api_views.AddFeedback.as_view()),
        url(r'^api/listfeedback/$', api_views.ListFeedback.as_view()),
        url(r'^api/getfeedback/(?P<pk>[0-9]+)/$', api_views.EditFeedback.as_view()),

# FOR USer Interest
        # for adding intrest
        url(r'^api/adduserintreset/$', api_views.AddUserintreset.as_view()),
        url(r'^api/listuserintreset/$', api_views.ListUserintreset.as_view()),
        url(r'^api/getuserintreset/(?P<pk>[0-9]+)/$', api_views.EditUserintreset.as_view()),
        url(r'^userdetails/(?P<pk>[0-9]+)/$', views.userdetails, name='userdetails'),

# All list  of Interest of perticular user send user id as argument 
        url(r'^api/listuserintresetbyuser/(?P<userid>[0-9]+)/$', api_views.ListUserintresetbyuser.as_view()),

# list of interest of perticular user
        url(r'^api/listuserintresetbyusertoberead/(?P<userid>[0-9]+)/$', api_views.ListUserintresetbyusertoberead.as_view()),
        url(r'^api/listuserintresetbyuserreading/(?P<userid>[0-9]+)/$', api_views.ListUserintresetbyuserreading.as_view()),
        url(r'^api/listuserintresetbyuserread/(?P<userid>[0-9]+)/$', api_views.ListUserintresetbyuserread.as_view()),

# threadcount All list  of Interest of perticular user send user id as argument 
        url(r'^listuserintresetbyuser/(?P<userid>[0-9]+)/$', views.ListUserintresetbyuser, name='ListUserintresetbyuser'),
        url(r'^listuserintresetbyusertoberead/(?P<userid>[0-9]+)/$', views.ListUserintresetbyusertoberead,name='ListUserintresetbyusertoberead'),
        url(r'^listuserintresetbyuserreading/(?P<userid>[0-9]+)/$', views.ListUserintresetbyuserreading,name='ListUserintresetbyuserreading'),
        url(r'^listuserintresetbyuserread/(?P<userid>[0-9]+)/$', views.ListUserintresetbyuserread,name='listuserintresetbyuserread'),
        # url(r'^adminpage/$', views.adminpage, name='adminpage'),
        url(r'^listpodcastbooks/(?P<podcastid>\w+)/$', views.Listpodcastbooks,name='listpodcastbooks'),

        # url(r'^adminpage/$', views.adminpage, name='adminpage'),
#========================= for Podcast ==========================

        url(r'^api/addpodcast/$', api_views.Addpodcast.as_view()),
        url(r'^api/listpodcast/(?P<userid>[0-9]+)/$', api_views.Listpodcast.as_view()),
        url(r'^api/editpodcast/(?P<pk>\w+)/$', api_views.Editpodcast.as_view()),
        url(r'^api/deletepodcast/(?P<pk>\w+)/$', api_views.deletepodcast.as_view()),

        url(r'^api/addpodcastbooks/$', api_views.Addpodcastbooks.as_view()),
        url(r'^api/listpodcastbooks/(?P<podcastid>\w+)/$', api_views.Listpodcastbooks.as_view()),
        url(r'^api/editpodcastbooks/(?P<pk>\w+)/$', api_views.Editpodcastbooks.as_view()),
        url(r'^api/deletepodcastbooks/(?P<pk>\w+)/$', api_views.deletepodcastbooks.as_view()),

#------ for podcast threads --------------------------------------------

        url(r'^api/Addpodcast_thread/$', api_views.Addpodcast_thread.as_view()),
        url(r'^api/Editpodcast_thread/(?P<pk>\w+)/$', api_views.Editpodcast_thread.as_view()),
        url(r'^api/deletepodcast_thread/(?P<pk>\w+)/$', api_views.deletepodcast_thread.as_view()),
        url(r'^api/Listpodcast_thread/(?P<podcastid>\w+)/$', api_views.Listpodcast_thread.as_view()),

)
