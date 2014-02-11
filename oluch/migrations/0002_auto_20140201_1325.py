# encoding: utf-8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submit',
            old_name='author',
            new_name='uthor',
        ),
    ]
