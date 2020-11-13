from rest_framework import serializers

from threadcard.models import User,Category,Bookcover,Thread,SubComment,Rating,Subscribe,Feedback,Userintreset,Podcast,Podcastbooks,PodcastThread



#--------------------------USER----------------------------------

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class UsersubSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','email')

#-------------------------CATEGORY-----------------------------------

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

#-------------------------BOOKCOVER-----------------------------------

class BookcoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookcover
        fields = "__all__"

class BookcoverfullSerializer(serializers.ModelSerializer):
    created_by = UsersubSerializer(read_only=True)
    updated_by = UsersubSerializer (read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Bookcover
        fields = "__all__"

class BookcoversubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookcover
        fields = ('id','name')

#------------------------THREAD BITS---------------------------------

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"

class ThreadfullSerializer(serializers.ModelSerializer):
    bookcoverwoner = UsersubSerializer(read_only=True)
    updated_by = UsersubSerializer (read_only=True)
    bookcover = BookcoversubSerializer(read_only=True)
    class Meta:
        model = Thread
        fields = "__all__"

class ThreadsubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ('id','name')

#--------------------------SUB Comments--------------------------------

class SubCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubComment
        fields = "__all__"

class SubCommentfullSerializer(serializers.ModelSerializer):
    created_by = UsersubSerializer(read_only=True)
    updated_by = UsersubSerializer (read_only=True)
    class Meta:
        model = SubComment
        fields = "__all__"

class SubCommentsubSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubComment
        fields = ('id','comment')
        
#------------------Comments-Rating --------------------------------

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"

class RatingfullSerializer(serializers.ModelSerializer):
    created_by = UsersubSerializer(read_only=True)
    updated_by = UsersubSerializer (read_only=True)
    class Meta:
        model = Rating
        fields = "__all__"

class RatingsubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id','comment')


#-------------------------Subscribe-----------------------------------

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = "__all__"

class SubscribefullSerializer(serializers.ModelSerializer):
    writter = UsersubSerializer(read_only=True)
    reader = UsersubSerializer (read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Subscribe
        fields = "__all__"

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"

class FeedbackfullSerializer(serializers.ModelSerializer):
    created_by = UsersubSerializer(read_only=True)
    class Meta:
        model = Feedback
        fields = "__all__"

class UserintresetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userintreset
        fields = "__all__"

class UserintresetfullSerializer(serializers.ModelSerializer):
    user = UsersubSerializer(read_only=True)
    class Meta:
        model = Userintreset
        fields = "__all__"

#============== for Podcast ==============================

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = "__all__"

class PodcastfullSerializer(serializers.ModelSerializer):
    created_by = UsersubSerializer(read_only=True)
    class Meta:
        model = Podcast
        fields = "__all__"

class PodcastbooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcastbooks
        fields = "__all__"

class PodcastbooksfullSerializer(serializers.ModelSerializer):
    user = UsersubSerializer(read_only=True)
    class Meta:
        model = Podcastbooks
        fields = "__all__"

#============== for Podcast threads==============================

class PodcastThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastThread
        fields = "__all__"

class PodcastThreadfullSerializer(serializers.ModelSerializer):
    created_by = UsersubSerializer(read_only=True)
    class Meta:
        model = PodcastThread
        fields = "__all__"
