from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from threadcard.models import TwitterUserProfile
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404

from django.http import Http404

import twitter

consumer_key = 'RUVp98TCLxU9S4ONTFiIJHmKx' 
consumer_secret =  'ogsjD40xApMK0omrta9FdcbSv3Qb8vkQzbtSJq6ZyeJ7EGhin9'

# consumer_key = 'gxJ0DrgnvciGseKdqdGoZjk0f' 
# consumer_secret =  'HnmAg62OvaDXh2aKJv5YWZHanxL83umxSWiZeocLDrZvuyxb9N'



def index(request):
    if request.user.is_authenticated():
        return render(request, 'home.html', {'name': request.user.first_name})
    else:
        # Show an error page
        return render(request, 'login.html')

def adminlogin(request):
    context = RequestContext(request)
    context_dict = { }
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            if user.username == "Admin":
                # Redirect to a success page.
                return HttpResponseRedirect("threadcard/adminpage")
        else:
            # Show an error page
            return render(request, 'login.html', {'error': 'you Dont have access !!'})

    return render_to_response('adminlogin.html', context_dict, context)


def signup(request):
    email = request.POST['signup_email']
    password = request.POST['signup_password']
    first_name = request.POST['signup_first_name']
    last_name = request.POST['signup_last_name']
    username = email

    try:
        user = User.objects.create_user(
        username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return HttpResponseRedirect("/home", {'success': 'Successfully LoggedIn.'})
    except IntegrityError:
        return render(request, 'login.html', {'error': 'User already exists!! Try forgot password.'})



def signin(request):
    print "user request", request.user.is_authenticated()
    if request.user.is_authenticated():
        u=request.user
        user_name=u.username
        twitteruser=UserSocialAuth.objects.get(user=u)
        uid=twitteruser.uid
        data= twitteruser.extra_data
        print data

        access_token_secret = data["access_token"]["oauth_token_secret"]
        access_token_key = data["access_token"]["oauth_token"]
        oauth_user_id = data["access_token"]["user_id"]
        oauth_id = data["id"]
        screen_name = data["access_token"]["screen_name"]
        api = twitter.Api(consumer_key=consumer_key,consumer_secret=consumer_secret,access_token_key=access_token_key,access_token_secret=access_token_secret)
        data = api.VerifyCredentials()
        image = data.profile_image_url
        print "dwwdw",image
        try:
            user_profile=TwitterUserProfile.objects.get(user=u)
            user_profile.profile_image_url=image
            user_profile.save()
        except TwitterUserProfile.DoesNotExist:
            userprofile = TwitterUserProfile(user=u,profile_image_url=image)
            userprofile.save()
        return HttpResponseRedirect("/"+user_name+"/home")
        # return HttpResponseRedirect("../"+user_name+"/home")
                
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            if user.username == "Admin":
                # Redirect to a success page.
                return HttpResponseRedirect("threadcard/adminpage")
        else:
            # Show an error page
            return render(request, 'login.html', {'error': 'you Dont have access !!'})
    else:
        return render(request, 'login.html')


# def signin(request):
#     print request.user.is_authenticated()
#     if request.user.is_authenticated():
#         u=request.user
#         print "============="
#         twitteruser=UserSocialAuth.objects.get(user=u)
#         uid=twitteruser.uid
#         data= twitteruser.extra_data
#         access_token_secret = data["access_token"]["oauth_token_secret"]
#         access_token_key = data["access_token"]["oauth_token"]
#         oauth_user_id = data["access_token"]["user_id"]
#         oauth_id = data["id"]
#         screen_name = data["access_token"]["screen_name"]
#         api = twitter.Api(consumer_key=consumer_key,consumer_secret=consumer_secret,access_token_key=access_token_key,access_token_secret=access_token_secret)
#         data = api.VerifyCredentials()
#         image = data.profile_image_url
#         try:
#             user_profile=TwitterUserProfile.objects.get(user=u)
#             user_profile.profile_image_url=image
#             user_profile.save()
#         except TwitterUserProfile.DoesNotExist:
#             userprofile = TwitterUserProfile(user=u,profile_image_url=image)
#             userprofile.save()
#         return HttpResponseRedirect("/home", {'success': 'Successfully LoggedIn.'})
                
#     if request.POST:
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(username=username, password=password)
#         if user is not None and user.is_active:
#             # Correct password, and the user is marked "active"
#             auth.login(request, user)
#             # Redirect to a success page.
#             return HttpResponseRedirect("/home", {'success': 'Successfully LoggedIn.'})
#         else:
#             # Show an error page
#             return render(request, 'login.html', {'error': 'Invalid user try signup!!'})
#     else:
#         return render(request, 'login.html')


def home(request,acti= None, **kwargs):
    print "user home"
    if request.user.is_authenticated():
        user_name=request.user.username
        return HttpResponseRedirect("/"+user_name+"/list")
        # return HttpResponseRedirect("threadcard/listcard")
    else:
        # Show an error page
        return HttpResponseRedirect("/signin", {'error': 'Invalid user please Signin!!'})


def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return render(request, 'login.html')

#from urllib.request import urlopen, Request
def profile(request):
    if request.user.is_authenticated():
        u=request.user
        # print "============="
        # twitteruser=UserSocialAuth.objects.get(user=u)
        # uid=twitteruser.uid
        # data= twitteruser.extra_data
        # access_token_secret = data["access_token"]["oauth_token_secret"]
        # access_token_key = data["access_token"]["oauth_token"]
        # oauth_user_id = data["access_token"]["user_id"]
        # oauth_id = data["id"]
        # screen_name = data["access_token"]["screen_name"]
        # api = twitter.Api(consumer_key=consumer_key,consumer_secret=consumer_secret,access_token_key=access_token_key,access_token_secret=access_token_secret)
        # data = api.VerifyCredentials()
        # image = data.profile_image_url
        
        # u.image=image
        # u.save()
        print u.twitter_profiles.profile_image_url
        print "======"

        return HttpResponseRedirect("/home", {'success': 'Successfully LoggedIn.'})
    else:
        return render(request, 'login.html')


def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
