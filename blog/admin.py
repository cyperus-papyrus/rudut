# coding=utf-8
from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)
admin.site.register(Category)


class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('author', 'title', 'text', ('created_date', 'published_date'),
                       'tags', 'meta_description', 'category', 'url')
        }),
        (u'Главная страница - картинки 140px', {
            'classes': ('collapse',),
            'fields': ('is_on_mainpage', 'image')
        }),
    )
