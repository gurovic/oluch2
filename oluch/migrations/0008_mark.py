# encoding: utf-8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0007_auto_20140202_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('sort_order', models.IntegerField(default=1000000)),
                ('contest', models.ForeignKey(to='oluch.Contest', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
