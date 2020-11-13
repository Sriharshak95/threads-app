from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.conf import settings
import random, string
# Create your models here.
class TwitterUserProfile(models.Model):
    """
    For users who login via Twitter.
    """
    # screen_name = models.CharField(max_length=200,unique=True,db_index=True)
    user = models.OneToOneField(User, related_name='twitter_profiles')
    # access_token = models.CharField(max_length=255,blank=True,null=True,editable=False)
    profile_image_url = models.URLField(blank=True, null=True)
    # location = models.TextField(blank=True, null=True)
    # url = models.URLField(blank=True, null=True)
    # description = models.CharField(max_length=160, blank=True, null=True)

    def __unicode__(self):
        return "%s's profile" % self.user



class Category(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table="Category"

def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Bookcover.objects.get(pk=short_id)
        except:
            return short_id

class Bookcover(models.Model):
    id = models.SlugField(max_length=6,primary_key=True,default=get_short_code,editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    updated_date= models.DateTimeField(blank=True, null=True)

    name = models.CharField(max_length=128,null=True, blank=True)
    tagline = models.CharField(max_length=128,null=True, blank=True)
    description = models.CharField(blank=True,max_length=512)
    url = models.URLField(null=True, blank=True)
    live = models.BooleanField(default=True)
    category = models.ForeignKey(Category,null=True, blank=True)
    thread_count = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    rating_sum = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True, upload_to='thredcards')

    def _get_average_rating(self):
        if self.rating_count == 0:
            return 0.0
        else:
            return round(float(self.rating_sum)/float(self.rating_count),1)

    rating_average = property(_get_average_rating)

    class Meta:
        db_table="Bookcover"

    def __unicode__(self):
        return self.name


class Thread(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date= models.DateTimeField(blank=True, null=True)
    bookcoverowner = models.ForeignKey(User)
    bookcover = models.ForeignKey(Bookcover)
    name = models.CharField(blank=True, null=True,max_length=64)
    message = models.CharField(max_length=500)
    live = models.BooleanField(default=True)
    subcomment_count = models.IntegerField(default=0)
    image = models.FileField(null=True, blank=True, upload_to='threads')
    author = models.CharField(max_length=128,blank=True)
    publisher = models.CharField(max_length=128,blank=True)

    class Meta:
        db_table="Thread"

    def __unicode__(self):
        return self.message

class SubComment(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    threadname = models.ForeignKey(Thread)
    updated_date= models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=200)
    live = models.BooleanField(default=True)
    image = models.FileField(null=True, blank=True, upload_to='subcomment')

    class Meta:
        db_table="SubComment"


RATING_CHOICES = ( (1,'1'),(2,'2'),
    (3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),
    (8,'8'),(9,'9'),(10,'10')
)

class Rating(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date= models.DateTimeField(blank=True, null=True)
    rater = models.ForeignKey(User)
    bookcover = models.ForeignKey(Bookcover)
    comment = models.CharField(max_length=200,null=True)
    like = models.BooleanField(default=False)

    def __unicode__(self):
        return self.comment

    class Meta:
        db_table="Rating"

#-----------------------------------------------------

class Subscribe(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    writter = models.ForeignKey(User,related_name="writter")
    reader = models.ForeignKey(User,related_name="reader")
    subscribe = models.BooleanField(default=False)


    class Meta:
        db_table="Subscribe"
        unique_together=(("writter","reader"),)

class Feedback(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,related_name="feedbackuser")
    email = models.EmailField(max_length=100)
    comment = models.CharField(max_length=500)
    url = models.CharField(max_length=200,blank=True, null=True)
    image = models.FileField(null=True, blank=True, upload_to='feedback')

    class Meta:
        db_table="Feedback"

#========================== User Intrest ================

class Userintreset(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    bookname = models.CharField(max_length=64,null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    weburl = models.URLField(null=True, blank=True)
    author = models.CharField(max_length=128,blank=True)
    publisher = models.CharField(max_length=128,blank=True)
    tagline = models.CharField(max_length=128,null=True, blank=True)
    description = models.CharField(blank=True,max_length=512)
    toberead = models.BooleanField(default=True)
    read = models.BooleanField(default=False)
    reading = models.BooleanField(default=False)
    comment = models.CharField(max_length=500,blank=True)

    class Meta:
        db_table="Userintreset"
        unique_together=(("user","bookname","author"),)

#========================= Podcast =======================

def get_podcast_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Podcast.objects.get(pk=short_id)
        except:
            return short_id

class Podcast(models.Model):
    id = models.SlugField(max_length= 6, primary_key= True, default= get_podcast_short_code, editable= False)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    updated_date= models.DateTimeField(blank= True, null= True)
    name = models.CharField(max_length= 64, null= True, blank= True)
    embed = models.CharField(blank= True, max_length= 512)
    likes = models.IntegerField(default= 0)

    class Meta:
        db_table="Podcast"
        unique_together=(("created_by","name"),)

    def __unicode__(self):
        return self.name


class Podcastbooks(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    podcast = models.ForeignKey(Podcast)
    bookname = models.CharField(max_length=128,null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    weburl = models.URLField(null=True, blank=True)
    author = models.CharField(max_length=128,blank=True)
    publisher = models.CharField(max_length=128,blank=True)
    tagline = models.CharField(max_length=128,null=True, blank=True)
    description = models.CharField(blank=True,max_length=512)

    class Meta:
        db_table="Podcastbooks"
        unique_together=(("user","podcast","bookname"),)

    def __unicode__(self):
        return self.bookname

class PodcastThread(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date= models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User)
    podcast = models.ForeignKey(Podcast)
    name = models.CharField(blank=True, null=True,max_length=64)
    message = models.CharField(max_length=500)
    live = models.BooleanField(default=True)
    subcomment_count = models.IntegerField(default=0,null=True)
    image = models.FileField(null=True, blank=True, upload_to='podcast_threads')

    class Meta:
        db_table="PodcastThread"

    def __unicode__(self):
        return self.message
