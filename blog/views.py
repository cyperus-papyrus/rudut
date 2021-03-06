# coding=utf-8
from django.utils import timezone
from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm
from ipware.ip import get_real_ip


def show_404(request):
    return render(request, 'blog/404.html')


def post_list(request):
    posts = Post.objects.filter(is_on_mainpage=True).filter(published_date__lte=timezone.now()
                                                            ).order_by('published_date')
    car_posts = Post.objects.filter(is_in_carousel=True).filter(published_date__lte=timezone.now()
                                                            ).order_by('published_date')
    feat_posts = Post.objects.filter(is_on_mainpage_500=True).filter(published_date__lte=timezone.now()
                                                            ).order_by('published_date')
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'feat_post': feat_posts, 'car_posts': car_posts,
                                                   'categories': categories})


def post_detail(request, url):
    post = get_object_or_404(Post, url=url)
    return render(request, 'blog/post_detail.html', {'post': post})


def tags(request, tag):
    posts = Post.objects.filter(tags__name__in=[tag])
    catg = Category.objects.all()
    what = u'по тегу'
    return render(request, 'blog/tags.html', {'posts': posts, 'tag': tag, 'categories': catg,
                                              'what': what})


def categories(request, category):
    posts = Post.objects.filter(category=category)
    name = Category.objects.filter(id=category)
    catg = Category.objects.all()
    what = u'из рубрики'
    return render(request, 'blog/category.html', {'posts': posts, 'tag': name, 'categories': catg,
                                              'what': what})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # Если форма заполнена корректно, сохраняем все введённые пользователем значения
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            message_to_user = message
            client_address = get_real_ip(request)
            message += '\n\n' + u'email отправителя: ' + sender + '\n' + u'ip отправителя: ' + client_address
            copy = form.cleaned_data['copy']

            recipient = ['robot@rudut.ru']
            u_recipient = []
            # Если пользователь захотел получить копию себе, добавляем его в список получателей
            if copy:
                u_recipient.append(sender)
            try:
                send_mail(subject, message, 'robot@rudut.ru', recipient)
                send_mail(subject, message_to_user, 'robot@rudut.ru', u_recipient)
            except BadHeaderError:  # Защита от уязвимости
                return HttpResponse('Invalid header found')
            # Переходим на другую страницу, если сообщение отправлено
            return render(request, 'blog/thanks.html')
    else:
        # Заполняем форму
        form = ContactForm()
    # Отправляем форму на страницу
    return render(request, 'blog/contact.html', {'form': form})
