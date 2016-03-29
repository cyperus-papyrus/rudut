from __future__ import unicode_literals
from django.conf.urls import include, url
from . import views
from django.conf.urls.static import static
from rudut import settings

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
