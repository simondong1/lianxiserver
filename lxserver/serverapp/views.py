from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from .models import User_profile
from .serializers import User_Serializer, User_profile_Serializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def signup(request):
    serializer = User_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        #username is number?
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"not found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)

    serializer = User_Serializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("got {}".format(request.user.password))

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
#client upload profile data, save in database
def create_profile(request):
    serializer = User_profile_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(request.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#update profile function for updating preferences

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
#provide recommendation based on user location
def get_recommendations(request):
    location = request.GET.get('location')
    if location is not None:
        try:
            location = int(location)
        except:
            return Response({"error": "Invalid location parameter. It should be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            #call database, get query set
            results = User_profile.objects.filter(location_bucket=location)

            #ranking logic (person to person matrix)

            #serialize query set to json
            serializer = User_profile_Serializer(results, many=True)

            return Response(serializer.data)
    else:
        return Response({"error": "No location parameter provided in the URL."},status=status.HTTP_400_BAD_REQUEST)