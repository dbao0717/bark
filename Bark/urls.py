"""Bark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from barks.views import (
    home_view, bark_detail_view, bark_list_view, 
    bark_create_view, bark_delete_view, bark_action_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('react/', TemplateView.as_view(template_name = 'react.html')),
    path('create-bark', bark_create_view),
    path('barks', bark_list_view),
    path('barks/<int:bark_id>', bark_detail_view),
    path('api/barks/<int:bark_id>/delete', bark_delete_view),
    path('api/barks/action', bark_action_view),
    path('api/barks/', include('barks.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)