# Generated by Django 2.0 on 2018-01-03 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20180102_1734'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='SiteUser',
        ),
    ]
