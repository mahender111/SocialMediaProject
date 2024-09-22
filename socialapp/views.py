from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db import models
from rest_framework import generics, status, permissions, filters, pagination
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework import serializers
from .models import FriendRequest, Friendship


from .serializers import (
    UserSignupSerializer, 
    UserLoginSerializer, 
    UserSerializer, 
    FriendRequestSerializer, 
    FriendRequestAcceptRejectSerializer,
    LogoutSerializer
)

# Create your views here.

def index(request):
    return HttpResponse("welcome to Social Media Network")


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class LoginpageView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': {
                'username': user.username,
                'email': user.email,
            }
        })


class LoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    

class SendFriendRequestView(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    print(queryset)
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print('cdff')
        receiver_id = self.request.data.get('receiver')
        print('receiver_id',receiver_id)
        receiver = get_object_or_404(User, id=receiver_id)
        print(receiver)

        if receiver == self.request.user:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")

        if FriendRequest.objects.filter(sender=self.request.user, receiver=receiver).exists():
            raise serializers.ValidationError("Friend request already sent.")

        serializer.save(sender=self.request.user, receiver=receiver, status='pending')


class UserSearchPagination(PageNumberPagination):
    page_size = 5


class UserListSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserSearchPagination
    filter_backends = [SearchFilter]
    search_fields = ['^username', '^email']


class AcceptRejectFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestAcceptRejectSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        friend_request = self.get_object()
        print('friend_request:', friend_request)
        
        status_action = request.data.get('status')  # Use a different name than 'status' to avoid conflicts
        print('status_action:', status_action)

        if status_action not in ['accepted', 'rejected']:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        sender = friend_request.sender
        print('sender',sender)
        receiver = friend_request.receiver
        print('receiver',receiver)

        # Ensure the receiver is the current authenticated user
        if receiver == request.user:
            print('uuuuuuuuuuuuuuuu')
            return Response({"error": "You are not authorized to respond to this friend request."}, status=status.HTTP_403_FORBIDDEN)

        if status_action == 'accepted':
            print('rrrrrrrrrrrrrrr')
            Friendship.objects.create(user1=receiver, user2=sender)
            friend_request.delete()  # Remove the friend request after accepting
            return Response({"message": "Friend request accepted."}, status=status.HTTP_200_OK)

        elif status_action == 'rejected':
            print('hhhhhhhhh')
            friend_request.delete()
            return Response({"message": "Friend request rejected."}, status=status.HTTP_200_OK)
        



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the user's token
        try:
            token = Token.objects.get(user=request.user)
            # Delete the token to log the user out
            token.delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)
        
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             request.user.auth_token.delete()
#             return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutpageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            Token.objects.get(user=user).delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)






# =------------------------------------------------------------------------------------------------------------------------
# class AcceptRejectFriendRequestView(APIView):
#     def post(self, request, pk):
#         try:
#             friend_request = FriendRequest.objects.get(pk=pk)
#             print(friend_request)
#         except FriendRequest.DoesNotExist:
#             return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = FriendRequestAcceptRejectSerializer(friend_request, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class AcceptRejectFriendRequestView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
    
#     def AcceptRejectFriend(self, serializer):
#         friend_request = self.request.data.get('sender')
#         print(sender_id)
#         receiver = get_object_or_404(User, id=sender_id)
#         print(receiver)

    # def post(self, request, pk):
    #     try:
    #         friend_request = FriendRequest.objects.get(pk=pk)
    #         print(friend_request)
    #     except FriendRequest.DoesNotExist:
    #         return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = FriendRequestAcceptRejectSerializer(friend_request, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------------------


# class SignupView(APIView):
#     def post(self, request):
#         serializer = UserSignupSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
    # 


# from django.contrib.auth import login

# class LoginView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             login(request, user)
#             return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# class UserDetailView(APIView):
#     def get(self, request, user_id):
#         user = User.objects.get(id=user_id)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
    






# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from rest_framework.authtoken.models import Token
# from .serializers import UserSignupSerializer, UserSerializer

# class SignupView(generics.CreateAPIView):
#     serializer_class = UserSignupSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             "token": token.key,
#             "user": UserSerializer(user).data
#         }, status=status.HTTP_201_CREATED)

# ------------------------------------------------------------

# from django.db import models
# from django.contrib.auth.models import User

# class UserSession(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     login_time = models.DateTimeField(auto_now_add=True)
#     logout_time = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.login_time}"
    
# from .models import UserSession

# class LoginView(generics.CreateAPIView):
#     serializer_class = UserLoginSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)

#         # Create a UserSession record
#         UserSession.objects.create(user=user)

#         return Response({
#             "token": token.key,
#             "user": UserSerializer(user).data
#         }, status=status.HTTP_200_OK)


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         user = request.user
#         try:
#             # Update the UserSession record to include logout time
#             session = UserSession.objects.get(user=user, logout_time__isnull=True)
#             session.logout_time = timezone.now()
#             session.save()
            
#             # Delete the token to log the user out
#             Token.objects.get(user=user).delete()
#             return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
#         except Token.DoesNotExist:
#             return Response({"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)
#         except UserSession.DoesNotExist:
#             return Response({"detail": "No active session found."}, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.views import APIView

# class ActiveUsersView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         active_sessions = UserSession.objects.filter(logout_time__isnull=True).select_related('user')
#         active_users = [{'username': session.user.username, 'login_time': session.login_time} for session in active_sessions]
#         return Response(active_users, status=status.HTTP_200_OK)

# class HandleFriendRequestView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         friend_request = FriendRequest.objects.get(id=kwargs['request_id'])
#         if friend_request.receiver != request.user:
#             return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

#         if request.data.get('action') == 'accept':
#             friend_request.is_accepted = True
#             friend_request.save()
#             Friendship.objects.create(user1=friend_request.sender, user2=friend_request.receiver)
#         else:
#             friend_request.delete()

#         return Response(status=status.HTTP_200_OK)

# class ListFriendsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         friendships = Friendship.objects.filter(user1=request.user) | Friendship.objects.filter(user2=request.user)
#         friends = [f.user2 if f.user1 == request.user else f.user1 for f in friendships]
#         serializer = UserSerializer(friends, many=True)
#         return Response(serializer.data)

# class ListPendingRequestsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         pending_requests = FriendRequest.objects.filter(receiver=request.user, is_accepted=False)
#         serializer = FriendRequestSerializer(pending_requests, many=True)
#         return Response(serializer.data)



# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         try:
#             request.user.auth_token.delete()
#             return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
#         except Token.DoesNotExist:
#             return Response({"error": "Token not found or user not logged in."}, status=status.HTTP_400_BAD_REQUEST)


# # View to log out a selected user
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]  # Ensure the user is authenticated to logout someone

#     def post(self, request, user_id, *args, **kwargs):
#         # Get the selected user
#         user = get_object_or_404(User, id=user_id)
        
#         # Invalidate the user's authentication token (if using token-based authentication)
#         try:
#             Token.objects.get(user=user).delete()
#             return Response({"message": f"User {user.username} has been successfully logged out."}, status=status.HTTP_200_OK)
#         except Token.DoesNotExist:
#             return Response({"message": f"Token not found for user {user.username}."}, status=status.HTTP_400_BAD_REQUEST)





# class LogoutView(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         user = request.user
#         print(user)
#         try:
#             Token.objects.get(user=user).delete()
#             return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
#         except Token.DoesNotExist:
#             return Response({"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)
        
# from django.contrib.auth import logout

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]  # Require the user to be authenticated
#     serializer_class = LogoutSerializer
#     def post(self, request, *args, **kwargs):
#         logout(request) 
#         return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]  # Require the user to be authenticated
#     serializer_class = LogoutSerializer

#     def post(self, request):
#         # Here, you can clear the session or handle token invalidation
#         logout(request)  # If using session-based auth

#         return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)



# class LogoutpageView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)