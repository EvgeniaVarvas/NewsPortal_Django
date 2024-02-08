from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from news.models import PostCategory


def get_subscribers(category):
    return category.subscribe.values_list('email', flat=True)


def new_post_subscription(instance):
    post_categories = PostCategory.objects.filter(post=instance)

    for post_category in post_categories:
        category = post_category.category
        email_subject = f'Новый пост в категории "{category}"'
        user_emails = get_subscribers(category)

        for email in user_emails:
            subject = email_subject
            message = render_to_string(
                template_name='news/new_post.html',
                context={'category': category, 'post': instance}
            )
            from_email = settings.DEFAULT_FROM_EMAIL

            send_mail(subject, message, from_email, [email])
