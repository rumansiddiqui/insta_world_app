# Generated by Django 4.1.7 on 2023-03-13 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_post_comments_alter_post_images_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
