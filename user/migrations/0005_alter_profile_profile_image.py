# Generated by Django 4.1.4 on 2023-02-09 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_profile_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='avator.png', upload_to='profile-images/'),
        ),
    ]
