from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

from .models import Bark
import random

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context = {}, status = 200)

def bark_list_view(request, *args, **kwargs):
    """
    Rest API View
    Consume by JavaScript/Swift/Java/iOS/Android
    Return json data
    """
    qs = Bark.objects.all()
    barks_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 1000)} for x in qs]
    data = {
        "isUser": False,
        "response": barks_list
    }
    return JsonResponse(data)

def bark_detail_view(request, bark_id, *args, **kwargs):
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