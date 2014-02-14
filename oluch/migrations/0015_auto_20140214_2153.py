# encoding: utf8
from django.db import models, migrations
import oluch.models


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0014_contest_statement_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='criteria_file',
            field=models.FileField(upload_to=oluch.models.criteria_filepath, null=True, verbose_name='Criteria', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contest',
            name='statement_file',
            field=models.FileField(upload_to=oluch.models.solutions_filepath, null=True, verbose_name='Statements', blank=True),
        ),
    ]
