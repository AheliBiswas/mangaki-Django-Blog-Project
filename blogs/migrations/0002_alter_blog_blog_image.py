# Generated by Django 4.1.4 on 2023-01-29 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_image',
            field=models.ImageField(default='demo.jpeg', upload_to='blog-images/'),
        ),
    ]
