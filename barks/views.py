from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url

from .models import Bark
from .forms import BarkForm
import random

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
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

def bark_create_view(request, *args, **kwargs):
    form = BarkForm(request.POST or None)
    next_url = request.POST.get("next") or None
    print("next_url", next_url)
    if form.is_valid():
        obj = form.save(commit = False)
        obj.save()
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = BarkForm()
    return render(request, 'components/form.html', context = {"form": form})

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