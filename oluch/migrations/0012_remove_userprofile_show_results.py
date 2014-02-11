# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oluch', '0011_auto_20140205_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='show_results',
        ),
    ]
