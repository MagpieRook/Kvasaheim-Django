# Generated by Django 2.0.7 on 2018-07-17 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kvasaheim', '0010_auto_20180716_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='spread',
        ),
    ]
