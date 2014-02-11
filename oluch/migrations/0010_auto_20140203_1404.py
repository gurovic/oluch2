# encoding: utf-8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0009_auto_20140203_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='show_results',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contest',
            name='accept_submits',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='contest',
            name='status',
        ),
    ]
