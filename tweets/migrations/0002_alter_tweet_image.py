# Generated by Django 4.0 on 2022-06-23 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='image',
            field=models.ImageField(blank=True, upload_to='tweet_images/'),
        ),
    ]
