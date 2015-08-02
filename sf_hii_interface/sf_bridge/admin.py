from django.contrib import admin

# Register your models here.
from .models import APIFromSF


class APIFromSFAdmin(admin.ModelAdmin):
    class Meta:
        model = APIFromSF


admin.site.register(APIFromSF, APIFromSFAdmin)
