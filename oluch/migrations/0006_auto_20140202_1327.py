# encoding: utf-8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0005_auto_20140202_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='sort_order',
            field=models.IntegerField(default=1000000),
        ),
    ]
