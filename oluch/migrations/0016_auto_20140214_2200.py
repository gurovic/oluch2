# encoding: utf8
from django.db import models, migrations
import oluch.models


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0015_auto_20140214_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='solutions_file',
            field=models.FileField(upload_to=oluch.models.solutions_filepath, null=True, verbose_name='Solutions', blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='contest',
            name='statement_file',
        ),
    ]
