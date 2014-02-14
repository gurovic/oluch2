# encoding: utf8
from django.db import models, migrations
import oluch.models
import oluch.settings


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0013_delete_mark'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='statement_file',
            field=models.FileField(default=oluch.settings.MEDIA_ROOT + '/empty.txt', upload_to=oluch.models.statements_filepath, verbose_name='Statements'),
            preserve_default=False,
        ),
    ]
