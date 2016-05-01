# coding=utf-8
from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)
admin.site.register(Category)


class Post(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('author', 'title', 'text', ('created_date', 'published_date'),
                       'tags', 'meta_description', 'category', 'url')
        }),
        (u'Карусель', {
            'classes': ('collapse',),
            'fields': ('is_in_carousel', 'image_background')
        }),
        (u'Главная страница - картинки 140px', {
            'classes': ('collapse',),
            'fields': ('is_on_mainpage', 'image')
        }),
        (u'Главная страница - картинки 500px', {
            'classes': ('collapse',),
            'fields': ('is_on_mainpage_500', 'image_500')
        }),
    )