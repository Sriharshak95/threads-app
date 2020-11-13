from threadcard.models import Thread
from django.http import HttpResponse
from .serializers import ThreadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#-------------Adding THread ----------------------

    #------ Threads-------
class ThreadList(APIView):
    def post(self, request, format=None):
        data = request.data
        for o in data:
            bookcoverid = o['bookcover']
            userid = o['bookcoverowner']
            serializer = ThreadSerializer(data=o)
            if serializer.is_valid():
                serializer.save()
                #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        print type(bookcoverid) , type(userid)
        threadcard = Thread.objects.filter(bookcoverowner_id= userid,bookcover_id=bookcoverid)
        serializer = ThreadSerializer(threadcard, many=True)
        return Response(serializer.data)


