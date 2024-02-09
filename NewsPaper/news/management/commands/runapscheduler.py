import logging
import datetime
from collections import defaultdict

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.conf import settings

from news.models import Post, Category

logger = logging.getLogger(__name__)


def my_job():
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


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fri', minute="00", hour="18"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
