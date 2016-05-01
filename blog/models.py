# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import smart_text
# Create your models here.
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
import logging
logger = logging.getLogger(__name__)


class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

    def __unicode__(self):
        return smart_text(self.category)


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = RichTextUploadingField(blank=True, default='')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to="blog/media/", default='/static/image/140.jpg')
    tags = TaggableManager()
    meta_description = models.CharField(max_length=200)
    is_in_carousel = models.BooleanField(default=False)
    image_background = models.ImageField(upload_to="blog/media/", default='media/blog/media/forest.jpg')
    is_on_mainpage = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    url = models.CharField(max_length=200, unique=True, null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return smart_text(self.title)

    class Meta:
        app_label = 'blog'
