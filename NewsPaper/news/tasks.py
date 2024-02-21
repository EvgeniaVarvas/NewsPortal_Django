from collections import defaultdict

from celery import shared_task
import datetime

from django.core.mail import EmailMultiAlternatives

from news.models import Post

from django.template.loader import render_to_string
from django.conf import settings


@shared_task
def new_post_subscription(post_id):
    post = Post.objects.get(pk=post_id)
    categories = post.categories.all()
    title = post.title
    subscribers_email = []

    for category in categories:
        subscribers = category.subscribe.all()
        for subscriber in subscribers:
            subscribers_email.append(subscriber.email)

    html_content = render_to_string(
        'news/new_post.html', {
            'text': f'{post.title}',
            'link': f'{settings.SITE_URL}post_detail/{post_id}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_email_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(created__gte=last_week)

    emails_by_user = defaultdict(list)

    for post in posts:
        categories = post.categories.all()
        for category in categories:
            subscribers = category.subscribe.all()
            for subscriber in subscribers:
                emails_by_user[subscriber.email].append(post)

    # Отправить почтовые сообщения каждому пользователю с их соответствующими постами
    for email, posts_for_user in emails_by_user.items():
        html = render_to_string(
            'news/daily_email.html', {
                'Link': settings.SITE_URL,
                'posts': posts_for_user,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Новое за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
