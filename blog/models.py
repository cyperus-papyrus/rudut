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
    category = models.CharField(max_length=200, verbose_name=u'Название раздела')

    def __str__(self):
        return self.category

    def __unicode__(self):
        return smart_text(self.category)

    class Meta:
        app_label = 'blog'
        verbose_name = u'Раздел'
        verbose_name_plural = u'Разделы'


class Post(models.Model):
    author = models.ForeignKey('auth.User', verbose_name=u'Автор', default=1)
    title = models.CharField(max_length=200, verbose_name=u'Заголовок поста')
    text = RichTextUploadingField(blank=True, default='', verbose_name=u'Текст')
    created_date = models.DateTimeField(default=timezone.now, verbose_name=u'Дата создания')
    published_date = models.DateTimeField(blank=True, null=True, verbose_name=u'Дата публикации',
                                          help_text=u'Если оставить пустым - запись не будет доступна пользователям')
    image = models.ImageField(upload_to="blog/media/", default='/static/image/140.jpg',
                              verbose_name=u'Превью 140px', help_text=u"Картинка-превью размером 140 px")
    image_500 = models.ImageField(upload_to="blog/media/", default='/static/image/140.jpg',
                                  verbose_name=u'Превью 500px', help_text=u"Картинка-превью размером 500 px")
    tags = TaggableManager(help_text=u"Вводить метки (теги) можно через пробел, либо через \
                                       запятую, или отделяя кавычками")
    meta_description = models.CharField(max_length=200, verbose_name=u'Мета тег "description"')
    is_in_carousel = models.BooleanField(default=False, verbose_name=u'Добавить в карусель')
    image_background = models.ImageField(upload_to="blog/media/", default='media/blog/media/forest.jpg',
                                         verbose_name=u'Фон в карусели', help_text=u"Картинка высотой 500 px")
    is_on_mainpage = models.BooleanField(default=False, verbose_name=u'Добавить на главную (140 px)')
    is_on_mainpage_500 = models.BooleanField(default=False, verbose_name=u'Добавить на главную (500 px)')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=u'Раздел')
    url = models.CharField(max_length=200, unique=True, null=True, blank=True, verbose_name=u'URL страницы',
                           help_text="Начальный и закрывающий / вводить НЕ нужно. Допустимы только латинские буквы, \
                           а так же символы -, _")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return smart_text(self.title)

    class Meta:
        app_label = 'blog'
        verbose_name = u'Пост'
        verbose_name_plural = u'Посты'
