# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0010_auto_20140203_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='short_title',
            field=models.CharField(default='01ots', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='title_en',
            field=models.CharField(default='no_en_title', max_length=200),
            preserve_default=True,
        ),
    ]
