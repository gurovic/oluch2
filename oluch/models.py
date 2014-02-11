import os

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    grade = models.IntegerField(_('grade'), max_length=2, blank=True, null=True)
    maxgrade = models.IntegerField(_('last grade at school'), max_length=2, default='11')
    school = models.CharField(_('school'), max_length=1000, blank=True, null=True)
    city = models.CharField(_('city'), max_length=1000, blank=True, null=True)
    country = models.CharField(_('country'), max_length=1000, default=_('Russia'))
                                                                   
    def __str__(self): 
        return self.user.username
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Contest(models.Model):
    title = models.CharField(max_length=200)         
    title_en = models.CharField(max_length=200, default="no_en_title")         
    short_title = models.CharField(max_length=200, default="01ots")         
    sort_order = models.IntegerField(default=1000000)
    accept_submits = models.NullBooleanField(default=False)
    show_results = models.NullBooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']


class Problem(models.Model):
    number = models.CharField(max_length=10)
    title = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=1000000) # order in the contest
    contest = models.ForeignKey(Contest, related_name='problem')

    def __str__(self):
        return self.number + (('. ' + self.title) if self.title else "")

    class Meta:
        ordering = ['contest', 'sort_order']


def filepath(instance, filename):
    return os.path.join(str(instance.problem.contest.id), str(instance.author.id), instance.problem.number + '.' + filename.split('.')[-1])

class Submit(models.Model):
    # submit description
    author = models.ForeignKey(User, related_name='submit')
    problem = models.ForeignKey(Problem)
    datetime = models.DateTimeField(auto_now_add=True)

    # marks info
    first_mark = models.IntegerField(default=-2) #-2: not evaluated yet, -1: is evaluatting just now
    first_judge = models.ForeignKey(User, related_name='first_mark_submit', blank=True, null=True)
    first_comment = models.CharField(max_length=1000, blank=True)
    second_mark = models.IntegerField(default=-2)
    second_judge = models.ForeignKey(User, related_name='second_mark_submit', blank=True, null=True)
    second_comment = models.CharField(max_length=1000, blank=True)
    third_judge = models.ForeignKey(User, related_name='third_mark_submit', blank=True, null=True)
    third_comment = models.CharField(max_length=1000, blank=True)
    final_mark = models.IntegerField(default=-2)

    #file info
    file = models.FileField(upload_to=filepath)

    def __str__(self):
        if hasattr(self.author, 'lastname'):
            result = self.author.lastname
        else:
            result = self.author.username
        
        if self.problem.title:
            result = result + ', #' + self.problem.number + '. ' + self.problem.title # + ': ' + self.file.url
        else:
            result = result + ', #' + self.problem.number # + ': '  + self.file.url

      
        return result + ' ' + str(self.first_mark) + '/' + str(self.second_mark) + str(self.final_mark)

class Mark(models.Model):
    title = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=1000000) # order in the contest
    contest = models.ForeignKey(Contest, related_name='mark')

    class Meta:
        ordering = ['contest', 'sort_order']
