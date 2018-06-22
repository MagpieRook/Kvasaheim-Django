# Generated by Django 2.0.1 on 2018-05-10 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('samplestatistics', '0003_auto_20180208_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='attempt',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='samplestatistics.Attempt'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='probleminstance',
            name='answer_string',
            field=models.TextField(),
        ),
    ]
