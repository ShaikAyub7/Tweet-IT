# Generated by Django 5.0.7 on 2024-07-24 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_tweet_follwers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='follwers',
            new_name='Follwers',
        ),
    ]
