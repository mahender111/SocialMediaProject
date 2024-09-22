from django.contrib import admin
from . models import FriendRequest,Friendship

# Register your models here. 

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['id','sender','receiver','timestamp','status']

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['id','user1','user2','created_at']

admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Friendship, FriendshipAdmin)