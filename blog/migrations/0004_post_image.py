# Generated by Django 3.2.7 on 2021-09-21 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to='featured_image/%Y/%m/%d/'),
        ),
    ]
