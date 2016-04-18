from django import forms
from django.forms import ModelForm

from .models import Media, Album


class MediaForm(ModelForm):
    class Meta:
        model = Media
        fields = ('content',)


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ('title', 'description',)


class dropDownForm(forms.Form):
    Albums = forms.ModelChoiceField(queryset=Album.objects.filter(user__id=1))

    def __init__(self, user, *args, **kwargs):
        super(dropDownForm, self).__init__(*args, **kwargs)
        print 'inside form'
        print user
        self.fields['Albums'].queryset = Album.objects.filter(user__id=user.id)
