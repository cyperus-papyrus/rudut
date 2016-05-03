# coding=utf-8
from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {
            'fields': ('author', 'title', 'text', ('created_date', 'published_date'),
                       'tags', 'meta_description', 'category', 'url',)
        }),
        ('Carousel', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('is_in_carousel', 'image_background',)
        }),
        ('Main page 140px', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('is_on_mainpage', 'image',)
        }),
        ('Main page 500px', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('is_on_mainpage_500', 'image_500',)
        }),
    )


class StackedItemInline(admin.StackedInline):
    classes = ('grp-collapse grp-open',)


class TabularItemInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
