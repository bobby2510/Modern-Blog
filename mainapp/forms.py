from django import forms
from .models import Post,Comment

class CreatePostForm(forms.ModelForm):
    title=forms.CharField(max_length=100,widget=forms.TextInput(
        attrs={
            'class':'fw size-30',
        }
    ))
    content=forms.CharField(max_length=5000,widget=forms.Textarea(
        attrs={
            'class':'fw size-400',
            'placeholder':'write here'
        }
    ))
    post_thumnail=forms.ImageField(label='thumbnail (optional):',required=False)
    class Meta:
        model=Post
        fields=['title','post_thumnail','content']
        
class CommentForm(forms.ModelForm):
    content=forms.CharField(label='',max_length=5000,widget=forms.Textarea(
        attrs={
            'class':'fw size-400',
            'placeholder':'comment here'
        }
    ))
    class Meta:
        model=Comment
        fields=['content',]
