# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from forms import UserForm
from models import User,Category,Bookcover,Thread,SubComment ,Rating,Subscribe

from django.shortcuts import render,render_to_response, get_object_or_404

from django.http import Http404

from django.contrib.auth.decorators import login_required
import json

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

    add_hero_cats_to_context_dict(context_dict)
    t = get_team(request.user)
    add_isteam_to_context_dict(context_dict, t)
    return render_to_response('index.html', context_dict, context)


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
        bookcover.thread_count = threadbit_count
        bookcover.rating_count = Rating.objects.filter(bookcover = bookcover).count()
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
    


@login_required
def edit_thread(request,pk,username):
# def edit_thread(request,pk,acti= None, **kwargs):
    # Request the context of the request.
    context = RequestContext(request)
    context_dict = { }

    user=request.user
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
    return HttpResponse(json.dumps(jsondata),content_type="application/json")

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
    return HttpResponse(json.dumps(jsondata),content_type="application/json")




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
            }

        bookcover.append(bookcover_data)

        # print "Book coverlist==",json.dumps(bookcover)

    user_data = { 'user': user.id,'username': user.username ,'user_profile':user_profile ,'totalthreadscreatedbyuser':totalthreadscreatedbyuser,
        'last_login':user.last_login.strftime("%A, %d. %B %Y %I:%M%p"),'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'date_joined':user.date_joined.strftime("%A, %d. %B %Y %I:%M%p"),'bookcover_data':bookcover }

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
            image = "null"

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





