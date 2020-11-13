__author__ = 'leif'

from django.contrib import admin
from threadcard.models import User,Category,Bookcover,Thread,SubComment,Rating

admin.site.register(Category)
admin.site.register(Bookcover)
admin.site.register(Thread)
admin.site.register(SubComment)
admin.site.register(Rating)
