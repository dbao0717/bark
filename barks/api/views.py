from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from ..models import Bark
from ..forms import BarkForm
from ..serializers import BarkSerializer, BarkActionSerializer, BarkCreateSerializer
import random

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.
@api_view(['POST']) # HTTP method from client == POST
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def bark_create_view(request, *args, **kwargs):
    serializer = BarkCreateSerializer(data = request.data)
    if serializer.is_valid(raise_exception = True):
        serializer.save(user = request.user)
        return Response(serializer.data, status = 201)
    return Response({}, status = 400)

@api_view(['GET'])
def bark_list_view(request, *args, **kwargs):
    qs = Bark.objects.all()
    username = request.GET.get('username')
    if username != None:
        qs = qs.filter(user__username__iexact = username)
    serializer = BarkSerializer(qs, many = True)
    return Response(serializer.data, status = 200)

@api_view(['GET'])
def bark_detail_view(request, bark_id, *args, **kwargs):
    qs = Bark.objects.filter(id = bark_id)
    if not qs.exists():
        return Response({}, status = 404)
    obj = qs.first()
    serializer = BarkSerializer(obj)
    return Response(serializer.data, status = 200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def bark_delete_view(request, bark_id, *args, **kwargs):
    qs = Bark.objects.filter(id = bark_id)
    if not qs.exists():
        return Response({}, status = 404)
    qs = qs.filter(user = request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this bark"}, status = 401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Bark has been deleted"}, status = 200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bark_action_view(request, *args, **kwargs):
    '''
    ID required
    Options: like, unlike, rebark
    '''
    print(request.POST, request.data)
    serializer = BarkActionSerializer(data = request.data)
    if (serializer.is_valid(raise_exception = True)):
        data = serializer.validated_data
        bark_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Bark.objects.filter(id = bark_id)
        if not qs.exists():
            return Response({}, status = 404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = BarkSerializer(obj)
            return Response(serializer.data, status = 200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = BarkSerializer(obj)
            return Response(serializer.data, status = 200)
        elif action == "rebark":
            new_bark = Bark.objects.create(user = request.user, parent = obj, content = content)
            serializer = BarkSerializer(new_bark)
            return Response(serializer.data, status = 201)
    return Response({}, status = 200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bark_feed_view(request, *args, **kwargs):
    user = request.user
    profiles = user.following.all()
    followed_users_id = []
    if profiles.exists():
        followed_users_id = [x.user.id for x in profiles]
    followed_users_id.append(user.id)
    qs = Bark.objects.filter(user__id__in=followed_users_id).order_by("-timestamp")
    serializer = BarkSerializer(qs, many = True)
    return Response(serializer.data, status = 200)