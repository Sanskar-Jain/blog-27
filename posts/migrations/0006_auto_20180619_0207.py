# Generated by Django 2.0.6 on 2018-06-19 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_read_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='read_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]