from django import forms
from .models import MakeTip
from django.forms import Textarea, TextInput, ImageField


class MakePostForm(forms.ModelForm):
    creativity = forms.IntegerField(required=False)
    sexy = forms.IntegerField(required=False)
    quality = forms.IntegerField(required=False)
    outfit = forms.IntegerField(required=False)
    post_pic = forms.FileField(required=True)

    class Meta:
        model = MakeTip
        fields = ['post_pic', 'title', 'creativity', 'sexy', 'quality', 'outfit']
        labels = {
            'post_pic': 'Selecciona video'
        }

        widgets = {
            'title': TextInput(attrs={'class': 'form-control'})
        }
