from turtle import textinput
from django import forms

from . import models


class SearchForm(forms.Form):
    '''
        Для поиска постов
    '''
    query = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'validationServer01',
    }))

class EmailPostForm(forms.Form):
    '''
        Для отправки на почту
    '''
    name = forms.CharField(max_length=25, widget= forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'validationServer01',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'id': 'validationServer02',
    }))
    to = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'id': 'validationServer03',
    }))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class':'form-control',
        'id': 'validationServer04',
    }))



class CommentForm(forms.ModelForm):
    '''
        Для сохранения комментариев
    '''
    class Meta:
        model = models.Comment

        fields = [
            'name', 
            'email', 
            'body',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'validationServer01',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'validationServer02',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'validationServer03',
            }),
        }