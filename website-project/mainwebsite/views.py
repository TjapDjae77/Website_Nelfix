from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import LoginSerializer, SelfSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render


def index(request):
    context = {
        'title':'Website Nelfix',
        'heading':'Pagie, World!',
    }
    return render(request, 'index.html', context)


# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.data['username']
#             password = serializer.data['password']
#             user = authenticate(username=username, password=password)
#             if user:
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     "status": "success",
#                     "message": "Login successful",
#                     "data": {
#                         "username": user.username,
#                         "token": str(refresh.access_token),
#                     }
#                 })
#             return Response({
#                 "status": "error",
#                 "message": "Invalid credentials"
#             }, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SelfView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         serializer = SelfSerializer(user)
#         return Response({
#             "status": "success",
#             "message": "User retrieved successfully",
#             "data": serializer.data
#         })