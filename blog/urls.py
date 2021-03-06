# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import include, url
from . import views
from django.conf.urls.static import static
from rudut import settings

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<url>[\w+-_]+)/$', views.post_detail, name='post_detail'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^posts/tag/(?P<tag>\w+)/$', views.tags, name='tags'),
    url(r'^category/(?P<category>[0-9]+)/$', views.categories, name='categories'),
    url(r'^contact/', views.contact, name='contact'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler403 = 'blog.views.show_404'
handler404 = 'blog.views.show_404'
