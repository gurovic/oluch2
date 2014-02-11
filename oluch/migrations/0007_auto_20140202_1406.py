# encoding: utf-8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0006_auto_20140202_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.IntegerField(default=0, choices=((0, 'Not started'), (1, 'Current, no results yet'), (2, 'Current, some results published'), (3, 'Finished, results published'), (4, 'Finished, no access'))),
        ),
    ]
