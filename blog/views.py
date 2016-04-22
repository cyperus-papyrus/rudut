# coding=utf-8
from django.utils import timezone
from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm


def post_list(request):
    posts = Post.objects.filter(is_on_mainpage=True).filter(published_date__lte=timezone.now()
                                                            ).order_by('published_date')
    car_posts = Post.objects.filter(is_in_carousel=True).filter(published_date__lte=timezone.now()
                                                            ).order_by('published_date')
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'car_posts': car_posts,
                                                   'categories': categories})


def post_detail(request, url):
    post = get_object_or_404(Post, url=url)
    return render(request, 'blog/post_detail.html', {'post': post})


def tags(request, tag):
    posts = Post.objects.filter(tags__name__in=[tag])
    catg = Category.objects.all()
    return render(request, 'blog/tags.html', {'posts': posts, 'tag': tag, 'categories': catg})


def categories(request, category):
    posts = Post.objects.filter(category=category)
    catg = Category.objects.all()
    return render(request, 'blog/tags.html', {'posts': posts, 'tag': category, 'categories': catg})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # Если форма заполнена корректно, сохраняем все введённые пользователем значения
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            message += '\n\n' + u'email отправителя: ' + sender
            copy = form.cleaned_data['copy']

            recipients = ['robot@rudut.ru']
            # Если пользователь захотел получить копию себе, добавляем его в список получателей
            if copy:
                recipients.append(sender)
            try:
                send_mail(subject, message, 'robot@rudut.ru', recipients)
            except BadHeaderError:  # Защита от уязвимости
                return HttpResponse('Invalid header found')
            # Переходим на другую страницу, если сообщение отправлено
            return render(request, 'blog/thanks.html')
    else:
        # Заполняем форму
        form = ContactForm()
    # Отправляем форму на страницу
    return render(request, 'blog/contact.html', {'form': form})
