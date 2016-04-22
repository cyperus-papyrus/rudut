# coding=utf-8
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    our_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(our_posts, 3)
    car_posts = Post.objects.filter(is_in_carousel=True).filter(published_date__lte=timezone.now()
                                                                ).order_by('published_date')
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
        categ = [p.category for p in our_posts]
    return render_to_response('blog/post_list.html', {'posts': posts, 'car_posts': car_posts})


def post_detail(request, url):
    post = get_object_or_404(Post, url=url)
    return render(request, 'blog/post_detail.html', {'post': post})


def tags(request, tag):
    posts = Post.objects.filter(tags__name__in=[tag])
    return render(request, 'blog/tags.html', {'posts': posts})


def categories(request, category):
    posts = Post.objects.filter(category__name__in=[category])
    return render(request, 'blog/tags.html', {'posts': posts})


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
