# Generated by Django 2.0.1 on 2018-05-17 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samplestatistics', '0004_auto_20180510_1240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comments',
            new_name='text',
        ),
    ]
