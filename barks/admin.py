from django.contrib import admin

# Register your models here.
from .models import Bark

class BarkAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']
    class Meta:
        model = Bark

admin.site.register(Bark, BarkAdmin)