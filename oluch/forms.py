from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User

from oluch.models import Submit

class SubmitForm(forms.Form):
    file = forms.FileField(label=_("Choose a file"))
    user = forms.HiddenInput()

    def __init__(self, choices, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        self.fields['problem'] = forms.ChoiceField(choices, label=_("Problem")) 


class UserInfoForm(forms.Form):
    username = forms.SlugField(max_length=20, label=_("Login"), widget=forms.TextInput(attrs={'size':'40'}))
    password1 = forms.SlugField(max_length=20, widget=forms.PasswordInput(attrs={'size':'40'}), label=_("Password"))
    password2 = forms.SlugField(max_length=20, widget=forms.PasswordInput(attrs={'size':'40'}), label=_("Password again"))
    lastname = forms.CharField(max_length=100, required=False, label=_("Last name"), widget=forms.TextInput(attrs={'size':'40'}))
    firstname = forms.CharField(max_length=100, required=False, label=_("Given name"), widget=forms.TextInput(attrs={'size':'40'}))
    grade = forms.CharField(max_length=1000, required=True, label=_("Grade"), widget=forms.TextInput(attrs={'size':'40'}))
    school = forms.CharField(max_length=1000, required=True, label=_("School"), widget=forms.TextInput(attrs={'size':'40'}))
    maxgrade = forms.CharField(max_length=1000, required=True, label=_("The last grade at your high school"), widget=forms.TextInput(attrs={'size':'40'}))
    city = forms.CharField(max_length=1000, required=True, label=_("City/settlement"), widget=forms.TextInput(attrs={'size':'40'}))
    country = forms.CharField(max_length=1000, required=True, label=_("Country"), widget=forms.TextInput(attrs={'size':'40'}))

    def clean(self):
        '''Required custom validation for the form.'''
        super(forms.Form, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                self._errors['password'] = [_('Passwords must match.')]
                self._errors['password_confirm'] = [_('Passwords must match.')]

        try:
            if set(self.cleaned_data["username"]) - set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'):
                self._errors['username'] = [_('Bad login.')]
            elif User.objects.filter(username=self.cleaned_data["username"]).count() > 0:
                self._errors['username'] = [_('User with such username already exists.')]
        except:
            self._errors['username'] = [_('Bad login.')]

        try:
            int(self.cleaned_data['grade'])
        except:
            self._errors['grade'] = [_('Grade must be a number.')]

        try:
            int(self.cleaned_data['maxgrade'])
        except:
            self._errors['maxgrade'] = [_('Grade must be a number.')]

        return self.cleaned_data