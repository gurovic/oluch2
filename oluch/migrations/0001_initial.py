# encoding: utf-8
from django.db import models, migrations
from django.conf import settings
import oluch.models


class Migration(migrations.Migration):
    
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Disqual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('public_comment', models.CharField(max_length=1000, blank=True)),
                ('private_comment', models.CharField(max_length=1000, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('sort_order', models.IntegerField()),
                ('contest', models.ForeignKey(to='oluch.Contest', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('problem', models.ForeignKey(to='oluch.Problem', to_field='id')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('first_mark', models.IntegerField(default=-2)),
                ('first_judge', models.ForeignKey(to_field='id', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('first_comment', models.CharField(max_length=1000, blank=True)),
                ('second_mark', models.IntegerField(default=-2)),
                ('second_judge', models.ForeignKey(to_field='id', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('second_comment', models.CharField(max_length=1000, blank=True)),
                ('third_judge', models.ForeignKey(to_field='id', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('third_comment', models.CharField(max_length=1000, blank=True)),
                ('final_mark', models.IntegerField(default=-2)),
                ('file', models.FileField(upload_to=oluch.models.filepath)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('grade', models.IntegerField(max_length=2, null=True, verbose_name='класс', blank=True)),
                ('maxgrade', models.IntegerField(default='11', max_length=2, verbose_name='номер последнего класса в школе')),
                ('school', models.CharField(max_length=1000, null=True, verbose_name='школа', blank=True)),
                ('city', models.CharField(max_length=1000, null=True, verbose_name='город', blank=True)),
                ('country', models.CharField(default='Россия', max_length=1000, verbose_name='страна')),
                ('show_results', models.BooleanField(default=True, verbose_name='показывать результаты')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
