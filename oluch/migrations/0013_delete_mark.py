# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [
        ('oluch', '0012_remove_userprofile_show_results'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Mark',
        ),
    ]
