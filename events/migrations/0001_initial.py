# Generated by Django 3.2.9 on 2021-11-29 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('repeat_event', models.CharField(choices=[('W', 'Weekly'), ('M', 'Monthly'), ('N', 'None')], default='N', max_length=1)),
                ('details', models.TextField()),
                ('base_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='LineupEventModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('performance_datetime', models.DateTimeField()),
            ],
        ),
    ]