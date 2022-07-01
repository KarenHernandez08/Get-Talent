from django.contrib import admin
from .models import AreasModel, RolesModel

# Register your models here.
admin.site.register(AreasModel)
admin.site.register(RolesModel)