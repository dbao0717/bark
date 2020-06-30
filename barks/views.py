from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

from .models import Bark

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context = {}, status = 200)

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