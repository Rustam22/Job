# Generated by Django 2.0 on 2017-12-20 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
