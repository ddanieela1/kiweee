# Generated by Django 4.1.3 on 2022-12-10 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_profile_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='media/kiwi-default-pic.jpeg', upload_to='', verbose_name='profile_imgs'),
        ),
    ]
