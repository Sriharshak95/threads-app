from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import serializers, viewsets, routers

from threadcard.models import User,Category,Bookcover,Thread,SubComment,Rating,Subscribe,Feedback,Userintreset,Podcast,Podcastbooks,PodcastThread

from .serializers import UsersubSerializer,UserSerializer,CategorySerializer,BookcoverSerializer,BookcoverfullSerializer,ThreadSerializer,ThreadfullSerializer,SubCommentSerializer,SubCommentfullSerializer

from .serializers import RatingSerializer,RatingfullSerializer,SubscribeSerializer,SubscribefullSerializer,FeedbackSerializer,FeedbackfullSerializer,UserintresetSerializer,UserintresetfullSerializer,PodcastSerializer,PodcastfullSerializer,PodcastbooksSerializer,PodcastbooksfullSerializer,PodcastThreadSerializer,PodcastThreadfullSerializer

class UserList(generics.ListCreateAPIView):
    """
    List all users, or create a new user.
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(generics.ListCreateAPIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        user = UserSerializer(user)
        return Response(user.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = User.objects.all()
    serializer_class = UsersubSerializer


#---------- Category MODEL --------------------

class AddCategory(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EditCategory(generics.RetrieveUpdateAPIView):
    # Get / Update a Choice
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

#------------BOOK COVER PAGE--------------------

class AddBookcover(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = Bookcover.objects.all()
    serializer_class = BookcoverSerializer

class ListBookcover(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = Bookcover.objects.all()
    serializer_class = BookcoverfullSerializer

class EditBookcover(generics.RetrieveUpdateAPIView):
    # Get / Update a Choice
    queryset = Bookcover.objects.all()
    serializer_class = BookcoverSerializer


class DeleteBookcover(generics.RetrieveDestroyAPIView):
    # Get / Update a Choice
    queryset = Bookcover.objects.all()
    serializer_class = BookcoverSerializer

#------------ Book Thread Bits--------------------

class AddThread(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

class EditThread(generics.RetrieveUpdateAPIView):
    # Get / Update a Choice
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

class ListThread(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = ThreadfullSerializer
    def get_queryset(self):
        bookcover=self.kwargs['bookcover']
        queryset=Thread.objects.filter(bookcover=bookcover)
        return queryset

class DeleteThread(generics.RetrieveDestroyAPIView):
    # Get / Update a Choice
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

#------------ Subcomment Threads--------------------

class AddSubComment(generics.ListCreateAPIView):
    # Get / Update a Choice
    # print "queryset======1"
    queryset = SubComment.objects.all()
    # print "queryset======2",queryset
    serializer_class = SubCommentSerializer
    # print ("serializer_class---------",serializer_class)

class EditSubComment(generics.RetrieveUpdateAPIView):
    # Get / Update a Choice
    queryset = SubComment.objects.all()
    serializer_class = SubCommentSerializer

class ListSubComment(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = SubCommentfullSerializer
    def get_queryset(self):
        threadid=self.kwargs['threadid']
        print "=====threadid=====",threadid
        queryset=SubComment.objects.filter(threadname=threadid)
        return queryset

class DeleteSubComment(generics.RetrieveDestroyAPIView):
    # Get / Update a Choice
    queryset = SubComment.objects.all()
    serializer_class = SubCommentSerializer


#------------ Subcomment Threads--------------------

class AddRating(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class EditRating(generics.RetrieveUpdateAPIView):
    # Get / Update a Choice
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class ListRating(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = RatingfullSerializer
    def get_queryset(self):
        bookcoverid=self.kwargs['bookcover']
        queryset=Rating.objects.filter(bookcover=bookcoverid)
        return queryset

#------------ Subscribe Threads--------------------

class AddSubscribe(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

class EditSubscribe(generics.RetrieveUpdateAPIView):
    # Get / Update a Choice
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

class ListSubscribe(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = SubscribefullSerializer
    def get_queryset(self):
        writterid=self.kwargs['userid']
        queryset=Subscribe.objects.filter(writter=writterid)
        return queryset

class UnSubscribe(generics.RetrieveDestroyAPIView):
    # Get / Update a Choice
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer


class CheckSubscribe(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = SubscribeSerializer
    def get_queryset(self):
        writterid=self.kwargs['from']
        readerid=self.kwargs['to']
        queryset=Subscribe.objects.filter(writter=writterid,reader=readerid)
        return queryset

#======== For Feedback

class AddFeedback(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class EditFeedback(generics.RetrieveUpdateAPIView):
    # Get / Update a Choice
    queryset = Feedback.objects.all()
    serializer_class = FeedbackfullSerializer

class ListFeedback(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = Feedback.objects.all()
    serializer_class = FeedbackfullSerializer

#========== FOR USER INTEREST===================

class AddUserintreset(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = Userintreset.objects.all()
    serializer_class = UserintresetSerializer

class EditUserintreset(generics.RetrieveUpdateAPIView):
    # Get / Update a Choice
    queryset = Userintreset.objects.all()
    serializer_class = UserintresetSerializer

class ListUserintreset(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = Userintreset.objects.all()
    serializer_class = UserintresetfullSerializer


class ListUserintresetbyuser(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = UserintresetfullSerializer
    def get_queryset(self):
        userid = self.kwargs['userid']
        queryset = Userintreset.objects.filter(user_id=userid)
        return queryset

class ListUserintresetbyuserreading(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = UserintresetfullSerializer
    def get_queryset(self):
        userid = self.kwargs['userid']
        queryset = Userintreset.objects.filter(user_id=userid,reading=True)
        return queryset

class ListUserintresetbyuserread(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = UserintresetfullSerializer
    def get_queryset(self):
        userid = self.kwargs['userid']
        queryset = Userintreset.objects.filter(user_id=userid,read=True)
        return queryset

class ListUserintresetbyusertoberead(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = UserintresetfullSerializer
    def get_queryset(self):
        userid = self.kwargs['userid']
        queryset = Userintreset.objects.filter(user_id=userid,toberead=True)
        return queryset
#========================= Podcast ===============================

class Addpodcast(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

class Editpodcast(generics.RetrieveUpdateAPIView):
    # Get / Update a Choice
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

class Listpodcast(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = PodcastfullSerializer
    def get_queryset(self):
        userid=self.kwargs['userid']
        queryset=Podcast.objects.filter(created_by_id=userid)
        return queryset

class deletepodcast(generics.RetrieveDestroyAPIView):
    # Get / Update a Choice
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer


class Addpodcastbooks(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = Podcastbooks.objects.all()
    serializer_class = PodcastbooksSerializer

class Editpodcastbooks(generics.RetrieveUpdateAPIView):
    # Get / Update a Choice
    queryset = Podcastbooks.objects.all()
    serializer_class = PodcastbooksSerializer

class Listpodcastbooks(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = PodcastbooksfullSerializer
    def get_queryset(self):
        podcastid=self.kwargs['podcastid']
        queryset=Podcastbooks.objects.filter(podcast_id=podcastid)
        return queryset

class deletepodcastbooks(generics.RetrieveDestroyAPIView):
    # Get / Update a Choice
    queryset = Podcastbooks.objects.all()
    serializer_class = PodcastbooksSerializer

#----------------------- for podcast threads----------------------------

class Addpodcast_thread(generics.ListCreateAPIView):
    # Get / Update a Choice
    queryset = PodcastThread.objects.all()
    serializer_class = PodcastThreadSerializer

class Editpodcast_thread(generics.RetrieveUpdateAPIView):
    # Get / Update a Choice
    queryset = PodcastThread.objects.all()
    serializer_class = PodcastThreadSerializer

class Listpodcast_thread(generics.ListCreateAPIView):
    # Get / Create questions
    serializer_class = PodcastThreadfullSerializer
    def get_queryset(self):
        podcastid=self.kwargs['podcastid']
        queryset=PodcastThread.objects.filter(podcast_id=podcastid)
        return queryset

class deletepodcast_thread(generics.RetrieveDestroyAPIView):
    # Get / Update a Choice
    queryset = PodcastThread.objects.all()
    serializer_class = PodcastThreadSerializer
