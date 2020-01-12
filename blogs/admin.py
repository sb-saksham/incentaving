from django.contrib import admin
from .models import Blog, Comments


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created']
    list_display_links = ['title']
    search_fields = ['content', 'title']
    list_filter = ['date_created']

    class Meta:
        model = Blog


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comments)
