# encoding: utf-8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0003_auto_20140201_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='sort_order',
            field=models.IntegerField(default=1000000),
            preserve_default=True,
        ),
    ]
