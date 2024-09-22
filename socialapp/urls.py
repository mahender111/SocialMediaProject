from django.urls import path
from . import views
from .views import ( 
    UserList,
    UserRetrieveUpdateDestroy,
    SignupView,
    LoginView,
    LoginpageView,

    LogoutView,
    LogoutpageView,
    SendFriendRequestView,
    UserListSearchView,
    AcceptRejectFriendRequestView

    )
    

urlpatterns = [
    path('',views.index, name='index_url'),
    path('userList/', UserList.as_view(), name='UserList_url'),
    path('user/<int:pk>/', UserRetrieveUpdateDestroy.as_view(), name='UserList_url'),

    path('SignupView/', SignupView.as_view(), name='SignupView_url'),
    path('LoginView/', LoginView.as_view(), name='LoginView_url'),
    path('LoginpageView/', LoginpageView.as_view(), name='LoginpageView_url'),

    path('LogoutView/', LogoutView.as_view(), name='LogoutView_url'),
    path('LogoutpageView/', LogoutpageView.as_view(), name='LogoutpageView'),

    path('send/', SendFriendRequestView.as_view(), name='SendFriendRequestView_url'),
    path('UserListSearch/', UserListSearchView.as_view(), name='UserListSearchView_url'),
    path('AcceptRejectFriendRequest/<int:pk>/', AcceptRejectFriendRequestView.as_view(), name='AcceptRejectFriendRequestView'),

]

