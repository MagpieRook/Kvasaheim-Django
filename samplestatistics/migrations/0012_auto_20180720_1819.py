# Generated by Django 2.0.7 on 2018-07-20 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samplestatistics', '0011_remove_problem_spread'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twolistproblem',
            name='second_spread',
        ),
        migrations.AddField(
            model_name='categoricalproblem',
            name='num_categories_high',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='categoricalproblem',
            name='num_categories_low',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
