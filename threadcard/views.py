# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from forms import UserForm
from models import User,Category,Bookcover,Thread,SubComment ,Rating,Subscribe,Feedback,Userintreset ,Podcast,Podcastbooks,PodcastThread
from django.contrib import auth

from django.shortcuts import render,render_to_response, get_object_or_404

from django.http import Http404

from django.contrib.auth.decorators import login_required
import json
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.views.decorators.clickjacking import xframe_options_exempt

# handling server exception 


def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)



def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    context_dict = { }
    # add_hero_cats_to_context_dict(context_dict)
    # t = get_team(request.user)
    # add_isteam_to_context_dict(context_dict, t)
    return render_to_response('index.html', context_dict, context)

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
                return HttpResponseRedirect("/adminpage")
        else:
            # Show an error page
            return render(request, 'login.html', {'error': 'you Dont have access !!'})


    return render_to_response('adminlogin.html', context_dict, context)



def category_show(request, catid):
    context = RequestContext(request)
    context_dict = { }
    add_hero_cats_to_context_dict(context_dict, catid)

    #demo_list = Demo.objects.filter(category=catid)
    cat_list = Category.objects.all()
    cat = Category.objects.get(id=catid)

    context_dict['cats']=cat_list
    context_dict['catid']=catid
    context_dict['cat']=cat

    t = get_team(request.user)
    add_isteam_to_context_dict(context_dict, t)

    return render_to_response('trail/index.html', context_dict, context)



@login_required
# def create_thread(request):
def create_thread(request,acti= None, **kwargs):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    user=request.user
    cardlist = Bookcover.objects.filter(created_by=user.id)  
    totalthreadscreatedbyuser = Bookcover.objects.filter(created_by=user.id).count()
    totalsubscribers = Subscribe.objects.filter(reader=user.id).count()
    SubscribedCreators = Subscribe.objects.filter(writter=user.id).count()
    context_dict['cardlist'] = cardlist
    context_dict['totalthreadscreatedbyuser']=totalthreadscreatedbyuser
    context_dict['SubscribedCreators']=SubscribedCreators
    context_dict['totalsubscribers']=totalsubscribers
    return render_to_response('createcard.html', context_dict, context)

@login_required
def adminpage(request):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    data = []
    users_list=User.objects.all()
    for user in users_list:     

        cardlist = Bookcover.objects.filter(created_by=user.id)
        totalthreadscreatedbyuser = Bookcover.objects.filter(created_by=user.id).count()
        try:
            if user.twitter_profiles:
                user_profile = user.twitter_profiles.profile_image_url
        except:
            user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

        # user_data = { 'user': user.id,'username': user.username ,'user_profile':user_profile ,'totalthreadscreatedbyuser':totalthreadscreatedbyuser,
        #     'last_login':user.last_login.strftime("%A, %d. %B %Y %I:%M%p"),'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'date_joined':user.date_joined.strftime("%A, %d. %B %Y %I:%M%p") }
        bookcover_list=[]
        for c in cardlist:
            bookcover = Bookcover.objects.get(id=c.id)
            threadbit_count = Thread.objects.filter(bookcover=bookcover).count()
            bookcover.thread_count = threadbit_count
            bookcover.rating_count = Rating.objects.filter(bookcover = bookcover).count()
            bookcover.likes = Rating.objects.filter(bookcover = bookcover,like=True).count()
            bookcover.save()

            request.META['HTTP_HOST']
            threads = Thread.objects.filter(bookcover_id=c.id)
            thread =[]
            if c.image :
                image = c.image.url
            else:
                image = "null"

            bookcover_data={ 'bookcoverid' : c.id,
                'created_date' : c.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
                'created_by' : str(c.created_by),
                'created_userid' : c.created_by.id,
                # 'updated_date': c.updated_date.strftime("%A, %d. %B %Y %I:%M%p"),
                'name': c.name ,
                'tagline' : c.tagline,
                'description' :c.description,
                'url ' : c.url,
                'live' : c.live,
                'category' : c.category,
                'thread_count' : c.thread_count,
                'rating_count' : c.rating_count,
                'likes' : c.likes,
                'image' : image,
                'thread': thread,
                }
            bookcover_list.append(bookcover_data)

        user_data = { 'user': user.id,'username': user.username ,'user_profile':user_profile ,'totalthreadscreatedbyuser':totalthreadscreatedbyuser,
            'last_login':user.last_login.strftime("%A, %d. %B %Y %I:%M%p"),'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'date_joined':user.date_joined.strftime("%A, %d. %B %Y %I:%M%p"),'bookcover_data':bookcover_list }

        data.append(user_data)

    context_dict['data'] = data
    return render_to_response('adminpage.html', context_dict, context)


# def list_thread(request):
@login_required
def list_thread(request,acti= None, **kwargs):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    user=request.user
    cardlist = Bookcover.objects.filter(created_by=user.id)
    for card in cardlist:
        #print "threadbit",card,card.id
        bookcover = Bookcover.objects.get(id=card.id)
        threadbit_count = Thread.objects.filter(bookcover=bookcover).count()
        bookcover.rating_count = Rating.objects.filter(bookcover = bookcover).count()
        bookcover.likes = Rating.objects.filter(bookcover = bookcover,like=True).count()
        bookcover.save()
    totalthreadscreatedbyuser = Bookcover.objects.filter(created_by=user.id).count()
    totalsubscribers = Subscribe.objects.filter(reader=user.id).count()
    SubscribedCreators = Subscribe.objects.filter(writter=user.id).count()
    context_dict['totalsubscribers']=totalsubscribers
    context_dict['SubscribedCreators']=SubscribedCreators
    context_dict['cardlist'] = cardlist
    context_dict['totalthreadscreatedbyuser']=totalthreadscreatedbyuser
    return render_to_response('listcard.html', context_dict, context)

@login_required
def list(request,user_name):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    # print "-----------",user_name
    user = request.user
    try:
        creator=User.objects.get(username=user_name)
        # print "iiii---",user.id
        cardlist = Bookcover.objects.filter(created_by=creator.id)
        for card in cardlist:
            # print "threadbit",card,card.id
            bookcover = Bookcover.objects.get(id=card.id)
            threadbit_count = Thread.objects.filter(bookcover=bookcover).count()
            bookcover.thread_count = threadbit_count
            bookcover.rating_count = Rating.objects.filter(bookcover = bookcover).count()
            bookcover.likes = Rating.objects.filter(bookcover = bookcover,like=True).count()
            bookcover.save()
        totalthreadscreatedbyuser = Bookcover.objects.filter(created_by=creator.id).count()
        totalsubscribers = Subscribe.objects.filter(reader=creator.id).count()
        SubscribedCreators = Subscribe.objects.filter(writter=creator.id).count()
        context_dict['totalsubscribers']=totalsubscribers
        context_dict['SubscribedCreators']=SubscribedCreators
        context_dict['cardlist'] = cardlist
        context_dict['user'] = user
        context_dict['creator'] = creator
        context_dict['totalthreadscreatedbyuser']=totalthreadscreatedbyuser
        return render_to_response('listcard.html', context_dict, context)
    except Exception as e:
        return render_to_response('listcard.html', {"user not present"})
    


# @login_required
def edit_thread(request,pk,username):
# def edit_thread(request,pk,acti= None, **kwargs):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }

    user = request.user
    card = Bookcover.objects.get(id=pk)
    totalthreadscreatedbyuser = Bookcover.objects.filter(created_by=card.created_by).count()
    threads = Thread.objects.filter(bookcover=pk)
    for j in threads:
        thread = Thread.objects.get(pk=j.id)
        subcommentcount = SubComment.objects.filter(threadname=thread.id).count()
        thread.subcomment_count = subcommentcount
        thread.save()
    subcomments = SubComment.objects.filter(threadname=Thread.objects.filter(bookcover=pk))
    same_threads = Bookcover.objects.filter(name=card.name)
    no_of_same_threads = Bookcover.objects.filter(name=card.name).count()
    context_dict['card'] = card
    context_dict['threads'] = threads
    context_dict['subcomments'] = subcomments
    context_dict['totalthreadscreatedbyuser'] = totalthreadscreatedbyuser
    context_dict['same_threads'] = same_threads
    context_dict['no_of_same_threads'] = no_of_same_threads
    return render_to_response('editcard.html', context_dict, context)

@login_required
def like_thread(request,pk):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    user=request.user
    card = Bookcover.objects.get(id=pk)
    data =[]
    try:
        rating = Rating.objects.get(bookcover=card,rater=user)
        rating.like = 1
        rating.save()
        card.likes = card.likes + 1
        card.save()
    except:
        rating = Rating(rater=user, bookcover=card, like="True" , comment="")
        rating.save()
        card.likes = card.likes + 1
        card.save()

    subdata={ 'rating_id':rating.id,'commented_date':rating.created_date.strftime("%A, %d. %B %Y %I:%M%p"),'commented_userid':rating.rater.id,'bookcover_id':card.id,'like':rating.like}
    data.append(subdata)
    jsondata={"data":data}
    return HttpResponse(json.dumps(data),content_type="application/json")

@login_required
def unlike_thread(request,pk):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    user=request.user
    card = Bookcover.objects.get(id=pk)
    data =[]
    rating = Rating.objects.get(bookcover=card,rater=user)
    rating.like = 0
    rating.save()
    card.likes = card.likes - 1
    card.save()
    subdata={ 'rating_id':rating.id,'commented_date':rating.created_date.strftime("%A, %d. %B %Y %I:%M%p"),'commented_userid':rating.rater.id,'bookcover_id':card.id,'like':rating.like}
    data.append(subdata)
    jsondata={"data":data}
    return HttpResponse(json.dumps(data),content_type="application/json")

def subcommentsList(request,threadid):
    request.META['HTTP_HOST']

    subcomment_list= SubComment.objects.filter(threadname=threadid)
    data = []
    for i in subcomment_list:
        try:
            if i.created_by.twitter_profiles:
                user_profile = i.created_by.twitter_profiles.profile_image_url
        except:
            user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

        subdata={ 'id':i.id,'commented_date':i.created_date.strftime("%A, %d. %B %Y %I:%M%p"),'commented_userid':str(i.created_by),'commented_user':i.created_by.username,'user_profile':user_profile,
                    'thread_id':i.threadname.id,'comment':i.comment}
        # print subdata
        data.append(subdata)
    jsondata={"data":data}
    return HttpResponse(json.dumps(data),content_type="application/json")

def threadList(request):
    user=request.user
    data = []
    cardlist = Bookcover.objects.filter(created_by=user.id)
    totalthreadscreatedbyuser = Bookcover.objects.filter(created_by=user.id).count()
    try:
        if user.twitter_profiles:
            user_profile = user.twitter_profiles.profile_image_url
    except:
        user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

    # user_data = { 'user': user.id,'username': user.username ,'user_profile':user_profile ,'totalthreadscreatedbyuser':totalthreadscreatedbyuser,
    #     'last_login':user.last_login.strftime("%A, %d. %B %Y %I:%M%p"),'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'date_joined':user.date_joined.strftime("%A, %d. %B %Y %I:%M%p") }
    bookcover_list=[]
    for c in cardlist:

        request.META['HTTP_HOST']
        threads = Thread.objects.filter(bookcover_id=c.id)
        thread =[]
        for t in threads :

            subcomment_userlist=[]
            subcommented_users = SubComment.objects.filter(threadname_id=t.id).values('created_by').distinct()
            for i in subcommented_users:
                user_id= i['created_by']
                commented_user=User.objects.get(id=user_id)

                try:
                    if commented_user.twitter_profiles:
                        user_profile = commented_user.twitter_profiles.profile_image_url
                except:
                    user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

                subcommented_user_data = { 'user': commented_user.id,'username':commented_user.username ,'user_profile':user_profile,
                    'first_name':commented_user.first_name,'last_name':commented_user.last_name,'email':commented_user.email }

                subcomment_userlist.append(subcommented_user_data)
    
            # print "subcomments==",json.dumps(subcomment_userlist)

            if t.image :
                image = t.image.url
            else:
                image = "null"


            thread_data = {
                'thread_bitid': t.id,
                'created_date':  t.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
                
                # 'updated_date': t.updated_date.strftime("%A, %d. %B %Y %I:%M%p"),
                
                'bookcoverowner': str(t.bookcoverowner),
                'bookcover' : str(t.bookcover),
                'name': t.name,
                'message': t.message,
                'live': t.live ,
                'subcomment_count': t.subcomment_count ,
                'image': image,
                'subcomment_userlist': subcomment_userlist
                }
            thread.append(thread_data)

        # print "Threads==",json.dumps(thread)
        maincomment_userlist=[]
        maincommented_users = Rating.objects.filter(bookcover_id=c.id).values('rater').distinct()
        for j in maincommented_users:
            user_id= j['rater']
            commented_user=User.objects.get(id=user_id)

            try:
                if commented_user.twitter_profiles:
                    user_profile = commented_user.twitter_profiles.profile_image_url
            except:
                user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

            maincommented_user_data = { 'user': commented_user.id,'username': commented_user.username ,'user_profile':user_profile,
                'first_name':commented_user.first_name,'last_name':commented_user.last_name,'email':commented_user.email }

            maincomment_userlist.append(maincommented_user_data)

        # print "main subcomments==",json.dumps(maincomment_userlist)
        if c.image :
            image = c.image.url
        else:
            image = "null"

        user= request.user
        try:
            rating = Rating.objects.get(bookcover=c,rater=user,like=True)
            liked= True
        except Exception as e:
            liked= False

        bookcover_data={ 'bookcoverid' : c.id,
            'created_date' : c.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
            'created_by' : str(c.created_by),
            'created_userid' : c.created_by.id,
            # 'updated_date': c.updated_date.strftime("%A, %d. %B %Y %I:%M%p"),
            'name': c.name ,
            'tagline' : c.tagline,
            'description' :c.description,
            'url ' : c.url,
            'live' : c.live,
            'category' : c.category,
            'thread_count' : c.thread_count,
            'rating_count' : c.rating_count,
            'likes' : c.likes,
            'image' : image,
            'thread': thread,
            'maincomment_userlist': maincomment_userlist,
            'liked':liked,
            }
        bookcover_list.append(bookcover_data)

        # print "Book coverlist==",json.dumps(bookcover)

    user_data = { 'user': user.id,'username': user.username ,'user_profile':user_profile ,'totalthreadscreatedbyuser':totalthreadscreatedbyuser,
        'last_login':user.last_login.strftime("%A, %d. %B %Y %I:%M%p"),'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'date_joined':user.date_joined.strftime("%A, %d. %B %Y %I:%M%p"),'bookcover_data':bookcover_list}

    # print "User coverlist==",json.dumps(user_data)

    jsondata={"data":user_data}
    return HttpResponse(json.dumps(jsondata),content_type="application/json")

def allthreadList(request):
    # user=request.user
    data = []
    users_list=User.objects.all()
    for user in users_list:     

        cardlist = Bookcover.objects.filter(created_by=user.id)
        totalthreadscreatedbyuser = Bookcover.objects.filter(created_by=user.id).count()
        try:
            if user.twitter_profiles:
                user_profile = user.twitter_profiles.profile_image_url
        except:
            user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

        # user_data = { 'user': user.id,'username': user.username ,'user_profile':user_profile ,'totalthreadscreatedbyuser':totalthreadscreatedbyuser,
        #     'last_login':user.last_login.strftime("%A, %d. %B %Y %I:%M%p"),'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'date_joined':user.date_joined.strftime("%A, %d. %B %Y %I:%M%p") }
        bookcover =[]
        for c in cardlist:

            request.META['HTTP_HOST']
            threads = Thread.objects.filter(bookcover_id=c.id)
            thread =[]
            for t in threads :

                subcomment_userlist=[]
                subcommented_users = SubComment.objects.filter(threadname_id=t.id).values('created_by').distinct()
                for i in subcommented_users:
                    user_id= i['created_by']
                    commented_user=User.objects.get(id=user_id)

                    try:
                        if commented_user.twitter_profiles:
                            user_profile = commented_user.twitter_profiles.profile_image_url
                    except:
                        user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

                    subcommented_user_data = { 'user': commented_user.id,'username':commented_user.username ,'user_profile':user_profile,
                        'first_name':commented_user.first_name,'last_name':commented_user.last_name,'email':commented_user.email }

                    subcomment_userlist.append(subcommented_user_data)
        
                # print "subcomments==",json.dumps(subcomment_userlist)

                if t.image :
                    image = t.image.url
                else:
                    image = "null"


                thread_data = {
                    'thread_bitid': t.id,
                    'created_date':  t.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
                    
                    # 'updated_date': t.updated_date.strftime("%A, %d. %B %Y %I:%M%p"),
                    
                    'bookcoverowner': str(t.bookcoverowner),
                    'bookcover' : str(t.bookcover),
                    'name': t.name,
                    'message': t.message,
                    'live': t.live ,
                    'subcomment_count': t.subcomment_count ,
                    'image': image,
                    'subcomment_userlist': subcomment_userlist
                    }
                thread.append(thread_data)

            # print "Threads==",json.dumps(thread)
            maincomment_userlist=[]
            maincommented_users = Rating.objects.filter(bookcover_id=c.id).values('rater').distinct()
            for j in maincommented_users:
                user_id= j['rater']
                commented_user=User.objects.get(id=user_id)

                try:
                    if commented_user.twitter_profiles:
                        user_profile = commented_user.twitter_profiles.profile_image_url
                except:
                    user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

                maincommented_user_data = { 'user': commented_user.id,'username': commented_user.username ,'user_profile':user_profile,
                    'first_name':commented_user.first_name,'last_name':commented_user.last_name,'email':commented_user.email }

                maincomment_userlist.append(maincommented_user_data)

            # print "main subcomments==",json.dumps(maincomment_userlist)
            if c.image :
                image = c.image.url
            else:
                image = "null"

            user= request.user
            try:
                rating = Rating.objects.get(bookcover=c,rater=user,like=True)
                liked= True
            except Exception as e:
                liked= False

            bookcover_data={ 'bookcoverid' : c.id,
                'created_date' : c.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
                'created_by' : str(c.created_by),
                'created_userid' : c.created_by.id,
                # 'updated_date': c.updated_date.strftime("%A, %d. %B %Y %I:%M%p"),
                'name': c.name ,
                'tagline' : c.tagline,
                'description' :c.description,
                'url ' : c.url,
                'live' : c.live,
                'category' : c.category,
                'thread_count' : c.thread_count,
                'rating_count' : c.rating_count,
                'likes' : c.likes,
                'image' : image,
                'thread': thread,
                'maincomment_userlist': maincomment_userlist,
                'liked':liked,
                }

            bookcover.append(bookcover_data)

            # print "Book coverlist==",json.dumps(bookcover)

        user_data = { 'user': user.id,'username': user.username ,'user_profile':user_profile ,'totalthreadscreatedbyuser':totalthreadscreatedbyuser,
            'last_login':user.last_login.strftime("%A, %d. %B %Y %I:%M%p"),'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'date_joined':user.date_joined.strftime("%A, %d. %B %Y %I:%M%p"),'bookcover_data':bookcover }

        data.append(user_data)
        # print "User coverlist==",json.dumps(user_data)

    jsondata={"data":data}
    return HttpResponse(json.dumps(jsondata),content_type="application/json")

def perticularthreadList(request,userid):
    data = []
    try:
        user=User.objects.get(id=userid)
    except:
        user_data="user not preset"
        jsondata={"data":user_data}
        return HttpResponse(json.dumps(jsondata),content_type="application/json")

    cardlist = Bookcover.objects.filter(created_by=user.id)
    totalthreadscreatedbyuser = Bookcover.objects.filter(created_by=user.id).count()
    try:
        if user.twitter_profiles:
            user_profile = user.twitter_profiles.profile_image_url
    except:
        user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"
    m=0
    bookcover = []

    for c in cardlist:
    #   print m,"===== Card Book",c.name,c.id

        request.META['HTTP_HOST']
        threads = Thread.objects.filter(bookcover_id=c.id)
        subcomment_count = Thread.objects.filter(bookcover_id=c.id).count()
        #print "subcomment_count==",subcomment_count
        thread =[]
        for t in threads :

            subcomment_userlist=[]
            subcommented_users = SubComment.objects.filter(threadname_id=t.id).values('created_by').distinct()
            for i in subcommented_users:
                user_id= i['created_by']
                commented_user=User.objects.get(id=user_id)

                try:
                    if commented_user.twitter_profiles:
                        user_profile = commented_user.twitter_profiles.profile_image_url
                except:
                    user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

                subcommented_user_data = { 'user': commented_user.id,'username':commented_user.username ,'user_profile':user_profile,
                    'first_name':commented_user.first_name,'last_name':commented_user.last_name,'email':commented_user.email }

                subcomment_userlist.append(subcommented_user_data)
    
            # print "subcomments==",json.dumps(subcomment_userlist)

            if t.image :
                image = t.image.url
            else:
                image = "null"


            thread_data = {
                'thread_bitid': t.id,
                'created_date':  t.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
                
                # 'updated_date': t.updated_date.strftime("%A, %d. %B %Y %I:%M%p"),
                
                'bookcoverowner': str(t.bookcoverowner),
                'bookcover' : str(t.bookcover),
                'name': t.name,
                'message': t.message,
                'live': t.live ,
                'subcomment_count': subcomment_count ,
                'image': image,
                'subcomment_userlist': subcomment_userlist
                }
            thread.append(thread_data)
        maincomment_userlist=[]
        maincommented_users = Rating.objects.filter(bookcover_id=c.id).values('rater').distinct()
        for j in maincommented_users:
            user_id= j['rater']
            commented_user=User.objects.get(id=user_id)

            try:
                if commented_user.twitter_profiles:
                    user_profile = commented_user.twitter_profiles.profile_image_url
            except:
                user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

            maincommented_user_data = { 'user': commented_user.id,'username': commented_user.username ,'user_profile':user_profile,
                'first_name':commented_user.first_name,'last_name':commented_user.last_name,'email':commented_user.email }

            maincomment_userlist.append(maincommented_user_data)

        # print "main subcomments==",json.dumps(maincomment_userlist)
        if c.image :
            image = c.image.url
        else:
            image = c.url

        user= request.user
        try:
            rating = Rating.objects.get(bookcover=c,rater=user,like=True)
            liked= True
        except Exception as e:
            liked= False


        same_threads_created_by=[]
        no_threads_count = Bookcover.objects.filter(name=c.name).count()
        same_threads = Bookcover.objects.filter(name=c.name)
        for k in same_threads :
            try:
                if k.created_by.twitter_profiles:
                    user_profile = k.created_by.twitter_profiles.profile_image_url
            except:
                user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

            same_threads_data ={
            'threadid' : k.id,
            'bookname' : k.name,
            'created_by' : k.created_by.username,
            'created_userid' : k.created_by.id,
            'user_profile' : user_profile
            }
            same_threads_created_by.append(same_threads_data)

        bookcover_data={
            'bookcoverid' : c.id,
            'created_date' : c.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
            'created_by' : str(c.created_by),
            'created_userid' : c.created_by.id,
            # 'updated_date': c.updated_date.strftime("%A, %d. %B %Y %I:%M%p"),
            'name': c.name ,
            'tagline' : c.tagline,
            'description' :c.description,
            'url ' : c.url,
            'live' : c.live,
            'category' : c.category,
            'thread_count' : c.thread_count,
            'rating_count' : c.rating_count,
            'likes' : c.likes,
            'image' : image,
            'thread': thread,
            'maincomment_userlist': maincomment_userlist,
            'liked':liked,
            'no_threads_count': no_threads_count,
            'same_threads_created_by': same_threads_created_by
            }
        m = m+1

   #    print "=========",m,"//////////////",bookcover_data

        bookcover.append(bookcover_data)

    #   print "Book coverlist==",json.dumps(bookcover)

    user_data = { 'user':user.id,'username': user.username ,'user_profile':user_profile,'totalthreadscreatedbyuser':totalthreadscreatedbyuser,
        'last_login':user.last_login.strftime("%A, %d. %B %Y %I:%M%p"),'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'date_joined':user.date_joined.strftime("%A, %d. %B %Y %I:%M%p"),'bookcover_data':bookcover }

    # print "User coverlist==",json.dumps(user_data)

    jsondata={"data":user_data}
    return HttpResponse(json.dumps(user_data),content_type="application/json")


def listsubscribers(request,userid):
    subscribers_list= Subscribe.objects.filter(reader=userid)
    data = []
    for i in subscribers_list:
        try:
            if i.writter.twitter_profiles:
                user_profile = i.writter.twitter_profiles.profile_image_url
        except:
            user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

        subdata={ 'id':i.id,'userid':i.writter.id,'username':i.writter.username,'user_profile':user_profile}
        #print subdata
        data.append(subdata)
    jsondata={"data":data}
    return HttpResponse(json.dumps(data),content_type="application/json")

def subscribedlist(request,userid):
    subscribers_list= Subscribe.objects.filter(writter=userid)
    data = []
    for i in subscribers_list:
        try:
            if i.reader.twitter_profiles:
                user_profile = i.reader.twitter_profiles.profile_image_url
        except:
            user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

        subdata={ 'id':i.id,'userid':i.reader.id,'username':i.reader.username,'user_profile':user_profile}
        #print subdata
        data.append(subdata)
    jsondata={"data":data}
    return HttpResponse(json.dumps(data),content_type="application/json")
#======================
#===================== List of User Intrest API ================

def ListUserintresetbyuser(request,userid):
    userintrest_list = Userintreset.objects.filter(user_id=userid)
    data = []
    for i in userintrest_list:
        same_threads_created_by=[]
        no_threads_count = Bookcover.objects.filter(name=i.bookname).count()
        same_threads = Bookcover.objects.filter(name=i.bookname)
        for k in same_threads :
            try:
                if k.created_by.twitter_profiles:
                    user_profile = k.created_by.twitter_profiles.profile_image_url
            except:
                user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

            same_threads_data ={
            'threadid': k.id,
            'bookname' : k.name,
            'created_by' : k.created_by.username,
            'created_userid' : k.created_by.id,
            'user_profile' : user_profile
            }
            same_threads_created_by.append(same_threads_data)

        user_intrest={
        "userintresetid" : i.id,
        "created_date": i.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
        "bookname": i.bookname,
        "image": i.image,
        "weburl": i.weburl,
        "author": i.author,
        "publisher": i.publisher,
        "tagline": i.tagline,
        "description": i.description,
        "toberead": i.toberead,
        "read": i.read,
        "reading": i.reading,
        "comment": i.comment,
        'no_threads_count': no_threads_count,
        'same_threads_created_by': same_threads_created_by
        }

        data.append(user_intrest)

    jsondata={"data":data}
    return HttpResponse(json.dumps(data),content_type="application/json")

def ListUserintresetbyuserreading(request,userid):
    userintrest_list = Userintreset.objects.filter(user_id=userid,reading=True)
    data = []
    for i in userintrest_list:
        same_threads_created_by=[]
        no_threads_count = Bookcover.objects.filter(name=i.bookname).count()
        same_threads = Bookcover.objects.filter(name=i.bookname)
        for k in same_threads :
            try:
                if k.created_by.twitter_profiles:
                    user_profile = k.created_by.twitter_profiles.profile_image_url
            except:
                user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

            same_threads_data ={
            'threadid': k.id,
            'bookname' : k.name,
            'created_by' : k.created_by.username,
            'created_userid' : k.created_by.id,
            'user_profile' : user_profile
            }
            same_threads_created_by.append(same_threads_data)

        user_intrest={
        "userintresetid" : i.id,
        "created_date": i.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
        "bookname": i.bookname,
        "image": i.image,
        "weburl": i.weburl,
        "author": i.author,
        "publisher": i.publisher,
        "tagline": i.tagline,
        "description": i.description,
        "toberead": i.toberead,
        "read": i.read,
        "reading": i.reading,
        "comment": i.comment,
        'no_threads_count': no_threads_count,
        'same_threads_created_by': same_threads_created_by
        }

        data.append(user_intrest)

    jsondata={"data":data}
    return HttpResponse(json.dumps(data),content_type="application/json")

def ListUserintresetbyuserread(request,userid):
    userintrest_list = Userintreset.objects.filter(user_id=userid,read=True)
    data = []
    for i in userintrest_list:
        same_threads_created_by=[]
        no_threads_count = Bookcover.objects.filter(name=i.bookname).count()
        same_threads = Bookcover.objects.filter(name=i.bookname)
        for k in same_threads :
            try:
                if k.created_by.twitter_profiles:
                    user_profile = k.created_by.twitter_profiles.profile_image_url
            except:
                user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

            same_threads_data ={
            'threadid': k.id,
            'bookname' : k.name,
            'created_by' : k.created_by.username,
            'created_userid' : k.created_by.id,
            'user_profile' : user_profile
            }
            same_threads_created_by.append(same_threads_data)

        user_intrest={
        "userintresetid" : i.id,
        "created_date": i.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
        "bookname": i.bookname,
        "image": i.image,
        "weburl": i.weburl,
        "author": i.author,
        "publisher": i.publisher,
        "tagline": i.tagline,
        "description": i.description,
        "toberead": i.toberead,
        "read": i.read,
        "reading": i.reading,
        "comment": i.comment,
        'no_threads_count': no_threads_count,
        'same_threads_created_by': same_threads_created_by
        }

        data.append(user_intrest)

    jsondata={"data":data}
    return HttpResponse(json.dumps(data),content_type="application/json")

def ListUserintresetbyusertoberead(request,userid):
    userintrest_list = Userintreset.objects.filter(user_id=userid,toberead=True)
    data = []
    for i in userintrest_list:
        same_threads_created_by=[]
        no_threads_count = Bookcover.objects.filter(name=i.bookname).count()
        same_threads = Bookcover.objects.filter(name=i.bookname)
        for k in same_threads :
            try:
                if k.created_by.twitter_profiles:
                    user_profile = k.created_by.twitter_profiles.profile_image_url
            except:
                user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

            same_threads_data ={
            'threadid': k.id,
            'bookname' : k.name,
            'created_by' : k.created_by.username,
            'created_userid' : k.created_by.id,
            'user_profile' : user_profile
            }
            same_threads_created_by.append(same_threads_data)

        user_intrest={
        "userintresetid" : i.id,
        "created_date": i.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
        "bookname": i.bookname,
        "image": i.image,
        "weburl": i.weburl,
        "author": i.author,
        "publisher": i.publisher,
        "tagline": i.tagline,
        "description": i.description,
        "toberead": i.toberead,
        "read": i.read,
        "reading": i.reading,
        "comment": i.comment,
        'no_threads_count': no_threads_count,
        'same_threads_created_by': same_threads_created_by
        }

        data.append(user_intrest)

    jsondata={"data":data}
    return HttpResponse(json.dumps(data),content_type="application/json")




#=================================== PODCAST ===========================

def Listpodcastbooks(request,podcastid):
    podcastbook_list = Podcastbooks.objects.filter(podcast_id=podcastid)
    data =[]
    for l in podcastbook_list:
        same_threads_created_by=[]
        print l.bookname
        no_threads_count = Bookcover.objects.filter(name=l.bookname).count()
        same_threads = Bookcover.objects.filter(name=l.bookname)
        for k in same_threads :
            try:
                if k.created_by.twitter_profiles:
                    user_profile = k.created_by.twitter_profiles.profile_image_url
            except:
                user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

            same_threads_data ={
            'threadid': k.id,
            'bookname' : k.name,
            'created_by' : k.created_by.username,
            'created_userid' : k.created_by.id,
            'user_profile' : user_profile
            }
            same_threads_created_by.append(same_threads_data)

        podcast_details={
        "id" : l.id,
        "user_id": l.user.id,
        "username": l.user.username ,
        "bookname": l.bookname,
        "image": l.image,
        "weburl": l.weburl,
        "author": l.author,
        "publisher": l.publisher,
        "tagline": l.tagline,
        "description": l.description,
        "podcast": l.podcast.id,
        'no_threads_count': no_threads_count,
        'same_threads_created_by': same_threads_created_by
        }
        data.append(podcast_details)

    jsondata={"data":data}
    return HttpResponse(json.dumps(data),content_type="application/json")



@xframe_options_exempt
def podcast(request):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    data = []
    context_dict['data'] = data
    return render_to_response('podcast.html', context_dict, context)


def podcastbook(request,username,pk):
# def podcastbook(request,pk,acti= None, **kwargs):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }

    card = Bookcover.objects.get(id=pk)
    totalthreadscreatedbyuser = Bookcover.objects.filter(created_by=card.created_by).count()
    threads = Thread.objects.filter(bookcover=pk)
    for j in threads:
        thread = Thread.objects.get(pk=j.id)
        subcommentcount = SubComment.objects.filter(threadname=thread.id).count()
        thread.subcomment_count = subcommentcount
        thread.save()
    subcomments = SubComment.objects.filter(threadname=Thread.objects.filter(bookcover=pk))
    context_dict['card'] = card
    context_dict['threads'] = threads
    context_dict['subcomments']=subcomments
    context_dict['totalthreadscreatedbyuser']=totalthreadscreatedbyuser
    return render_to_response('podcast.html', context_dict, context)

def podcastlist(request,pk):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    data = []
    print "ssssss",pk
    b = Userintreset.objects.get(id=pk)
    print "-----"
    print b
    print b.bookname
    print "++++++"
    # c = Bookcover.objects.filter(name=b.bookname)
    # c = Bookcover.objects.get(id=pk)
    # if c.image :
    #     image = c.image.url
    # else:
    #     image = c.url


    # threads = Thread.objects.filter(bookcover_id=c.id)
    # subcomment_count = Thread.objects.filter(bookcover_id=c.id).count()
    # #print "subcomment_count==",subcomment_count
    # thread =[]
    # for t in threads :

    #     subcomment_userlist=[]
    #     subcommented_users = SubComment.objects.filter(threadname_id=t.id).values('created_by').distinct()
    #     for i in subcommented_users:
    #         user_id= i['created_by']
    #         commented_user=User.objects.get(id=user_id)

    #         try:
    #             if commented_user.twitter_profiles:
    #                 user_profile = commented_user.twitter_profiles.profile_image_url
    #         except:
    #             user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

    #         subcommented_user_data = { 'user': commented_user.id,'username':commented_user.username ,'user_profile':user_profile,
    #             'first_name':commented_user.first_name,'last_name':commented_user.last_name,'email':commented_user.email }

    #         subcomment_userlist.append(subcommented_user_data)

    #     # print "subcomments==",json.dumps(subcomment_userlist)

    #     if t.image :
    #         image = t.image.url
    #     else:
    #         image = "null"


    #     thread_data = {
    #         'thread_bitid': t.id,
    #         'created_date':  t.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
            
    #         # 'updated_date': t.updated_date.strftime("%A, %d. %B %Y %I:%M%p"),
            
    #         'bookcoverowner': str(t.bookcoverowner),
    #         'bookcover' : str(t.bookcover),
    #         'name': t.name,
    #         'message': t.message,
    #         'live': t.live ,
    #         'subcomment_count': subcomment_count ,
    #         'image': image,
    #         'subcomment_userlist': subcomment_userlist
    #         }
    #     thread.append(thread_data)
    # maincomment_userlist=[]
    # maincommented_users = Rating.objects.filter(bookcover_id=c.id).values('rater').distinct()
    # for j in maincommented_users:
    #     user_id= j['rater']
    #     commented_user=User.objects.get(id=user_id)

    #     try:
    #         if commented_user.twitter_profiles:
    #             user_profile = commented_user.twitter_profiles.profile_image_url
    #     except:
    #         user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

    #     maincommented_user_data = { 'user': commented_user.id,'username': commented_user.username ,'user_profile':user_profile,
    #         'first_name':commented_user.first_name,'last_name':commented_user.last_name,'email':commented_user.email }

    #     maincomment_userlist.append(maincommented_user_data)

    samebookuserslist =[]
    print "bookname",b.bookname
    samebookusers_list = Bookcover.objects.filter(name=b.bookname)
    print samebookusers_list,"0000000"
    for i in samebookusers_list:
        bookuser= User.objects.get(id=i.created_by_id)
        try:
            if bookuser.twitter_profiles:
                user_profile = bookuser.twitter_profiles.profile_image_url
        except:
            user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

        samebookuserslistdata={ 'id':i.id,'userid':bookuser.id,'username':bookuser.username,'user_profile':user_profile}
        print "======================"
        print samebookuserslistdata
        samebookuserslist.append(samebookuserslistdata)
    print samebookuserslist

    # bookcover_data={
    #     'bookcoverid' : c.id,
    #     'created_date' : c.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
    #     'created_by' : str(c.created_by),
    #     'created_userid' : c.created_by.id,
    #     # 'updated_date': c.updated_date.strftime("%A, %d. %B %Y %I:%M%p"),
    #     'name': c.name ,
    #     'tagline' : c.tagline,
    #     'description' :c.description,
    #     'url ' : c.url,
    #     'live' : c.live,
    #     'category' : c.category,
    #     'thread_count' : c.thread_count,
    #     'rating_count' : c.rating_count,
    #     'likes' : c.likes,
    #     'image' : image,
    #     'thread': thread,
    #     'maincomment_userlist': maincomment_userlist,
    #     }
    # data = {'bookcover_data':bookcover_data,'comment_userlist':maincomment_userlist,'samebookusers_list':samebookuserslist }
    data = {'samebookusers_list':samebookuserslist }

    jsondata={"data":data}
 
    return HttpResponse(json.dumps(samebookuserslist),content_type="application/json")


def sendemail(request,pk):
    context = RequestContext(request)
    context_dict = { }
    c = Bookcover.objects.get(id=pk)
    context['bookcover'] = c

    html_content = render_to_string('notificationemail.html', context=context).strip()

    subject = 'simple Email'
    from_email = 'manju24.rymec@gmail.com'
    reply_to = ['manju24.rymec@gmail.com']
    to = ['manju24j@gmail.com']
    msg = EmailMultiAlternatives(subject, html_content, to=to, from_email=from_email, reply_to=reply_to)  
    msg.content_subtype = 'html'   # Main content is text/html  
    msg.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!
    msg.send()
    print "email sent aytu"
    print msg
    return HttpResponse(msg)


def podcastthreadList(request,userid):
    data = []
    try:
        user=User.objects.get(id=userid)
    except:
        user_data="user not preset"
        jsondata={"data":user_data}
        return HttpResponse(json.dumps(jsondata),content_type="application/json")

    cardlist = Bookcover.objects.filter(created_by=user.id)
    totalthreadscreatedbyuser = Bookcover.objects.filter(created_by=user.id).count()
    try:
        if user.twitter_profiles:
            user_profile = user.twitter_profiles.profile_image_url
    except:
        user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"
    m=0
    bookcover = []

    for c in cardlist:
    #   print m,"===== Card Book",c.name,c.id

        request.META['HTTP_HOST']
        threads = Thread.objects.filter(bookcover_id=c.id)
        subcomment_count = Thread.objects.filter(bookcover_id=c.id).count()
        #print "subcomment_count==",subcomment_count
        thread =[]
        for t in threads :

            subcomment_userlist=[]
            subcommented_users = SubComment.objects.filter(threadname_id=t.id).values('created_by').distinct()
            for i in subcommented_users:
                user_id= i['created_by']
                commented_user=User.objects.get(id=user_id)

                try:
                    if commented_user.twitter_profiles:
                        user_profile = commented_user.twitter_profiles.profile_image_url
                except:
                    user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

                subcommented_user_data = { 'user': commented_user.id,'username':commented_user.username ,'user_profile':user_profile,
                    'first_name':commented_user.first_name,'last_name':commented_user.last_name,'email':commented_user.email }

                subcomment_userlist.append(subcommented_user_data)
    
            # print "subcomments==",json.dumps(subcomment_userlist)

            if t.image :
                image = t.image.url
            else:
                image = "null"


            thread_data = {
                'thread_bitid': t.id,
                'created_date':  t.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
                
                # 'updated_date': t.updated_date.strftime("%A, %d. %B %Y %I:%M%p"),
                
                'bookcoverowner': str(t.bookcoverowner),
                'bookcover' : str(t.bookcover),
                'name': t.name,
                'message': t.message,
                'live': t.live ,
                'subcomment_count': subcomment_count ,
                'image': image,
                'subcomment_userlist': subcomment_userlist
                }
            thread.append(thread_data)
        maincomment_userlist=[]
        maincommented_users = Rating.objects.filter(bookcover_id=c.id).values('rater').distinct()
        for j in maincommented_users:
            user_id= j['rater']
            commented_user=User.objects.get(id=user_id)

            try:
                if commented_user.twitter_profiles:
                    user_profile = commented_user.twitter_profiles.profile_image_url
            except:
                user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

            maincommented_user_data = { 'user': commented_user.id,'username': commented_user.username ,'user_profile':user_profile,
                'first_name':commented_user.first_name,'last_name':commented_user.last_name,'email':commented_user.email }

            maincomment_userlist.append(maincommented_user_data)

        # print "main subcomments==",json.dumps(maincomment_userlist)
        if c.image :
            image = c.image.url
        else:
            image = c.url

        bookcover_data={
            'bookcoverid' : c.id,
            'created_date' : c.created_date.strftime("%A, %d. %B %Y %I:%M%p"),
            'created_by' : str(c.created_by),
            'created_userid' : c.created_by.id,
            # 'updated_date': c.updated_date.strftime("%A, %d. %B %Y %I:%M%p"),
            'name': c.name ,
            'tagline' : c.tagline,
            'description' :c.description,
            'url ' : c.url,
            'live' : c.live,
            'category' : c.category,
            'thread_count' : c.thread_count,
            'rating_count' : c.rating_count,
            'likes' : c.likes,
            'image' : image,
            'thread': thread,
            'maincomment_userlist': maincomment_userlist
            }
        m = m+1

   #    print "=========",m,"//////////////",bookcover_data

        bookcover.append(bookcover_data)

    #   print "Book coverlist==",json.dumps(bookcover)

    user_data = { 'user':user.id,'username': user.username ,'user_profile':user_profile,'totalthreadscreatedbyuser':totalthreadscreatedbyuser,
        'last_login':user.last_login.strftime("%A, %d. %B %Y %I:%M%p"),'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'date_joined':user.date_joined.strftime("%A, %d. %B %Y %I:%M%p"),'bookcover_data':bookcover }

    # print "User coverlist==",json.dumps(user_data)

    jsondata={"data":user_data}
    return HttpResponse(json.dumps(user_data),content_type="application/json")

#=========================== PROJECTION ===========================
@xframe_options_exempt
def projection(request):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    data = []
    context_dict['data'] = data
    return render_to_response('projection.html', context_dict, context)


@login_required
def books(request,user_name):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    # print "-----------",user_name
    user = request.user
    try:
        creator=User.objects.get(username=user_name)
        # print "iiii---",user.id
        cardlist = Bookcover.objects.filter(created_by=creator.id)
        for card in cardlist:
            # print "threadbit",card,card.id
            bookcover = Bookcover.objects.get(id=card.id)
            threadbit_count = Thread.objects.filter(bookcover=bookcover).count()
            bookcover.thread_count = threadbit_count
            bookcover.rating_count = Rating.objects.filter(bookcover = bookcover).count()
            bookcover.likes = Rating.objects.filter(bookcover = bookcover,like=True).count()
            bookcover.save()
        totalthreadscreatedbyuser = Bookcover.objects.filter(created_by=creator.id).count()
        totalsubscribers = Subscribe.objects.filter(reader=creator.id).count()
        SubscribedCreators = Subscribe.objects.filter(writter=creator.id).count()
        context_dict['totalsubscribers']=totalsubscribers
        context_dict['SubscribedCreators']=SubscribedCreators
        context_dict['cardlist'] = cardlist
        context_dict['user'] = user
        context_dict['creator'] = creator
        context_dict['totalthreadscreatedbyuser']=totalthreadscreatedbyuser
        return render_to_response('books.html', context_dict, context)
    except Exception as e:
        return render_to_response('books.html', {"user not present"})

def createpodcast(request):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    data = []
    context_dict['data'] = data
    return render_to_response('createpodcast.html', context_dict, context)

def podcastpool(request):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    data = []
    context_dict['data'] = data
    return render_to_response('listpodcast.html', context_dict, context)

@xframe_options_exempt
def podcastshare(request):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    data = []
    context_dict['data'] = data
    return render_to_response('podcastshare.html', context_dict, context)
    
def userdetails(request,pk):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }
    data = []
    try:
        user=User.objects.get(id=pk)
        try:
            if user.twitter_profiles:
                user_profile = user.twitter_profiles.profile_image_url
        except:
            user_profile ="http://"+request.META['HTTP_HOST']+"/static/images/profile.png"

        data = { 'user': user.id,'username': user.username ,'user_profile':user_profile,'last_login':user.last_login.strftime("%A, %d. %B %Y %I:%M%p"),'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'date_joined':user.date_joined.strftime("%A, %d. %B %Y %I:%M%p")}
        return HttpResponse(json.dumps(data),content_type="application/json")

    except:
        user_data="user not preset"
        jsondata={"data":user_data}
        return HttpResponse(json.dumps(jsondata),content_type="application/json")