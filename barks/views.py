from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.
def home_view(request, *args, **kwargs):
    username = None
    if(request.user.is_authenticated):
        username = request.user.username
    return render(request, "pages/home.html", context = {"username": username}, status = 200)

def barks_list_view(request, *args, **kwargs):
    return render(request, "barks/list.html")

def barks_detail_view(request, bark_id, *args, **kwargs):
    return render(request, "barks/detail.html", context = {"bark_id": bark_id})

def barks_profile_view(request, username, *args, **kwargs):
    return render(request, "barks/profile.html", context = {"profile_username": username})

# def bark_create_view_pure_django(request, *args, **kwargs):
#     user = request.user
#     if not request.user.is_authenticated:
#         user = None
#         if request.is_ajax():
#             return JsonResponse({}, status = 401)
#         return redirect(settings.LOGIN_URL)
#     form = BarkForm(request.POST or None)
#     next_url = request.POST.get("next") or None
#     if form.is_valid():
#         obj = form.save(commit = False)
#         obj.user = user # Anonymous user
#         obj.save()
#         if request.is_ajax():
#             return JsonResponse(obj.serialize(), status = 201)
#         if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
#             return redirect(next_url)
#         form = BarkForm()
#     if form.errors:
#         if request.is_ajax():
#             return JsonResponse(form.errors, status = 400)
#     return render(request, 'components/form.html', context = {"form": form})

# def bark_list_view_pure_django(request, *args, **kwargs):
#     """
#     Rest API View
#     Consume by JavaScript/Swift/Java/iOS/Android
#     Return json data
#     """
#     qs = Bark.objects.all()
#     barks_list = [x.serialize() for x in qs]
#     data = {
#         "isUser": False,
#         "response": barks_list
#     }
#     return JsonResponse(data)

# def bark_detail_view_pure_django(request, bark_id, *args, **kwargs):
#     """
#     Rest API View
#     Consume by JavaScript/Swift/Java/iOS/Android
#     Return json data
#     """
#     data = {
#         "id": bark_id,
#     }
#     status = 200
#     try:
#         obj = Bark.objects.get(id = bark_id)
#         data['content'] = obj.content
#     except:
#         data['message'] = "Not found"
#         status = 404
    

#     return JsonResponse(data, status = status)