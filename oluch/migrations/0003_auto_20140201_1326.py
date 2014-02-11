# encoding: utf-8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0002_auto_20140201_1325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submit',
            old_name='uthor',
            new_name='author',
        ),
    ]
