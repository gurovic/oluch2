# encoding: utf-8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0004_contest_sort_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='sort_order',
            field=models.IntegerField(verbose_name=1000000),
        ),
    ]
