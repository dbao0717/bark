from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Bark
from .forms import BarkForm
from .serializers import BarkSerializer, BarkActionSerializer, BarkCreateSerializer
import random

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context = {}, status = 200)

@api_view(['POST']) # HTTP method from client == POST
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def bark_create_view(request, *args, **kwargs):
    serializer = BarkCreateSerializer(data = request.POST)
    if serializer.is_valid(raise_exception = True):
        serializer.save(user = request.user)
        return Response(serializer.data, status = 201)
    return Response({}, status = 400)

@api_view(['GET'])
def bark_list_view(request, *args, **kwargs):
    qs = Bark.objects.all()
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
        elif action == "rebark":
            new_bark = Bark.objects.create(user = request.user, parent = obj, content = content)
            serializer = BarkSerializer(new_bark)
            return Response(serializer.data, status = 200)
    return Response({}, status = 200)

def bark_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status = 401)
        return redirect(settings.LOGIN_URL)
    form = BarkForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit = False)
        obj.user = user # Anonymous user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status = 201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = BarkForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status = 400)
    return render(request, 'components/form.html', context = {"form": form})

def bark_list_view_pure_django(request, *args, **kwargs):
    """
    Rest API View
    Consume by JavaScript/Swift/Java/iOS/Android
    Return json data
    """
    qs = Bark.objects.all()
    barks_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": barks_list
    }
    return JsonResponse(data)

def bark_detail_view_pure_django(request, bark_id, *args, **kwargs):
    """
    Rest API View
    Consume by JavaScript/Swift/Java/iOS/Android
    Return json data
    """
    data = {
        "id": bark_id,
    }
    status = 200
    try:
        obj = Bark.objects.get(id = bark_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    

    return JsonResponse(data, status = status)