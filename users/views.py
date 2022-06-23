from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    LoginSerializer,RegisterSerializer, UserSerializer
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from .mixins import NoAuthenticationMixin


User = get_user_model()

class LoginView(NoAuthenticationMixin,generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.save()
        data = {
            "status": "success",
            "data": serializer.data,
            **tokens
        }
        return Response(data, status=status.HTTP_200_OK)


class RegisterView(NoAuthenticationMixin, generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            "status": "success",
            "message": "User created successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class FollowerView(APIView):
    
    def get_user(self, id):
        return get_object_or_404(User, id=id)

    def get(self, request, id):
        """
        get the no of followers of the user with the id
        """
        followers_no = len(self.get_user(id).followers.all())
        # print(self.get_user(id))
        data = {
            'status': 'success',
            'data': {
                'followers-count': followers_no
            }
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, id):
        """ 
            handles the authenticated user following the user with that id
        """
        user_to_follow = self.get_user(id)
        user_to_follow.followers.add(request.user)
        data = {
            'status': 'success',
            'data': [],
            'message': f'{request.user} follows {user_to_follow} successfully'
        }
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """
            handles removing the authenticated user from the followers list of the user with that id
        """
        user_to_follow = self.get_user(id)
        user_to_follow.followers.remove(request.user)
        data = {
            'status': 'success',
            'data': [],
            'message': f'{request.user} unfollows {user_to_follow} successfully'
        }
        return Response(data, status=status.HTTP_200_OK)


class FollowingView(APIView):

    def get_user(self, id):
        """
            get user using the id path parameter
        """
        return get_object_or_404(User, id=id)

    def get(self, request, id):
        """
        get the no of following  of the user with the id
        """
        following_no = len(self.get_user(id).following.all())
        data = {
            'status': 'success',
            'data': {
                'following-count': following_no
            }
        }
        return Response(data, status=status.HTTP_200_OK)

class ProfileView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_user(self, id):
        return get_object_or_404(User, id=id)
    
    def get(self, request, id):
        user = self.get_user(id)
        serializer = UserSerializer(user)
        data = {
            'status': 'success',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                'status': 'Successful',
                'data': serializer.data,
                'message': 'Profile Updated Successfully'
            }
            return Response(data, status.HTTP_200_OK)

LoginView = LoginView.as_view()
RegisterView = RegisterView.as_view()
ProfileView = ProfileView.as_view()
FollowerView = FollowerView.as_view()
FollowingView = FollowingView.as_view()