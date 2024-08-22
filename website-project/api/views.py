from user.models import Profile
from .serializers import FilmCreateSerializer, FilmListSerializer, FilmDetailSerializer, FilmUpdateSerializer, FilmDeleteSerializer, AdminLoginSerializer, UserSerializer, ProfileSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from film.models import Film
from rest_framework import status, permissions
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

# class UserLoginAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = authenticate(
#                 username=serializer.data['username'],
#                 password=serializer.data['password']
#             )
#             if user:
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     'status': 'success',
#                     'token': str(refresh.access_token),
#                 }, status=status.HTTP_200_OK)
#             return Response({"status": "error", "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'username': user.username,
                    'token': str(refresh.access_token),
                }
            }, status=200)
        return JsonResponse({'status': 'error', 'message': 'Invalid credentials', 'data': None}, status=401)
    
class FilmAPIListCreateView(ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]  # Add parsers to handle multipart file uploads

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(director__icontains=query))
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response({
            "status": "success",
            "message": "Film list fetched successfully",
            "data": data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print("Data received: ", request.data)
        serializer = FilmCreateSerializer(data=request.data)
        if serializer.is_valid():
            film = serializer.save()
            print("Film created: ", film)
            return Response({
                "status": "success",
                "message": "Film created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            print("Errors: ", serializer.errors)
        return Response({
            "status": "error",
            "message": serializer.errors,
            "data": None
        }, status=status.HTTP_400_BAD_REQUEST)

class FilmAPIDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        film = self.get_object()
        serializer = self.get_serializer(film)
        return Response({
            "status": "success",
            "message": "Film details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        print("Data received for update: ", request.data)
        film = self.get_object()
        serializer = FilmUpdateSerializer(film, data=request.data, partial=True)
        if serializer.is_valid():
            film = serializer.save()
            print("Film updated: ", film)
            return Response({
                "status": "success",
                "message": "Film updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            print("Errors: ", serializer.errors)
        return Response({
            "status": "error",
            "message": serializer.errors,
            "data": None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        film = self.get_object()
        serializer = FilmDeleteSerializer(film)
        data = serializer.data
        
        # Hapus video dan cover_image jika ada
        if film.video:
            film.video.delete(save=False)
        if film.cover_image:
            film.cover_image.delete(save=False)
        
        film.delete()

        return Response({
            "status": "success",
            "message": "Film deleted successfully",
            "data": data
        }, status=status.HTTP_204_NO_CONTENT)
    
# class UserListAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         query = request.query_params.get('q', None)
#         if query:
#             users = User.objects.filter(username__icontains=query)
#         else:
#             users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            users = User.objects.filter(username__icontains=query)
        else:
            users = User.objects.all()

        # Fetch profiles to get balance
        profiles = Profile.objects.filter(user__in=users)
        user_profiles = {profile.user.id: profile for profile in profiles}
        
        if not users.exists():
            return Response({
                "status": "error",
                "message": f"No users found matching the username '{query}'" if query else "No users found.",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        # Serialize users and attach balance information
        user_data = []
        for user in users:
            user_profile = user_profiles.get(user.id, None)
            balance = user_profile.balance if user_profile else 0
            user_data.append({
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'balance': balance
            })

        return Response({
            "status": "success",
            "message": "Users retrieved successfully",
            "data": user_data
        }, status=status.HTTP_200_OK)


class UserAPIDetailView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        user_id = self.kwargs.get('pk')
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return None
        return profile

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile is None:
            return Response({
                'status': 'error',
                'message': 'Profile not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(profile)
        return Response({
            'status': 'success',
            'message': 'User details retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class UserBalanceUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        profile = get_object_or_404(Profile, user__id=user_id)
        
        increment = request.data.get('increment', 0)
        
        if not isinstance(increment, int):
            return Response({
                "status": "error",
                "message": "Increment must be an integer",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if increment < 0:
            if profile.balance + increment < 0:
                return Response({
                    "status": "error",
                    "message": "Insufficient balance for the operation",
                    "data": None
                }, status=status.HTTP_400_BAD_REQUEST)
        
        profile.balance += increment
        profile.save()
        
        user_data = {
            "id": str(profile.user.id),
            "username": profile.user.username,
            "email": profile.user.email,
            "balance": profile.balance
        }
        
        return Response({
            "status": "success",
            "message": "Balance updated successfully",
            "data": user_data
        }, status=status.HTTP_200_OK)

class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        profile = get_object_or_404(Profile, user=user)
        
        # Serialize the profile data
        profile_data = {
            "id": str(profile.user.id),
            "username": profile.user.username,
            "email": profile.user.email,
            "balance": profile.balance
        }
        
        # Delete the user
        user.delete()
        
        return Response({
            "status": "success",
            "message": "User deleted successfully",
            "data": profile_data
        }, status=status.HTTP_200_OK)

class SelfRetrieveView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "User data retrieved successfully",
                "data": {
                    "username": user.username,
                    "token": str(refresh.access_token)
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"An error occurred: {str(e)}",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

