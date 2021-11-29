# Generated by Django 3.2.9 on 2021-11-29 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedbacks', '0001_initial'),
        ('events', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackmodel',
            name='addressed_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks_received', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feedbackmodel',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventmodel'),
        ),
        migrations.AddField(
            model_name='feedbackmodel',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks_sent', to=settings.AUTH_USER_MODEL),
        ),
    ]