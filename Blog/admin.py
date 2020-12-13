from django.contrib import admin
from .models import BlogManager,BlogHeight,BlogCategory
# Register your models here.

admin.site.register(BlogHeight)
admin.site.register(BlogManager)
admin.site.register(BlogCategory)
