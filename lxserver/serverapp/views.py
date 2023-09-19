from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        image_name = image.name
        with open(os.path.join('media', image_name), 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        return JsonResponse({'message': 'Image uploaded successfully.'})
    return JsonResponse({'error': 'Invalid request.'})

def get_image(request, usrname):
    #need to fix so run llm and find list of images with labels
    #  
    try:
        with open(os.path.join('media', usrname), 'rb') as image_file:
            response = HttpResponse(image_file.read(), content_type='image/jpeg')
            response['Content-Disposition'] = f'inline; filename="{usrname}"'
            return response
    except FileNotFoundError:
        return JsonResponse({'error': 'Image not found.'})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
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
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("got {}".format(request.user.password))