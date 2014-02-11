# encoding: utf-8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0008_mark'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Disqual',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=1000, null=True, verbose_name='city', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.CharField(max_length=1000, null=True, verbose_name='school', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='maxgrade',
            field=models.IntegerField(default='11', max_length=2, verbose_name='last grade at school'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='show_results',
            field=models.BooleanField(default=True, verbose_name='show results'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='grade',
            field=models.IntegerField(max_length=2, null=True, verbose_name='grade', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(default='Russia', max_length=1000, verbose_name='country'),
        ),
    ]
