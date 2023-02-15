from django.forms import ModelForm
from blogs.models import Blog,Comment
from django import forms

class CreateBlogForm(ModelForm):
    # title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title of your blog here'}))
    # # blog_genre' : forms.Select(attrs={'class':'form-control', 'placeholder':'Select a genre for the blog'}),
    # # tag' : forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Add tags'}),
    # blog_image = forms.MultipleChoiceField(widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta:
        model = Blog
        fields = ['title','description','blog_genre','blog_thumbnail','blog_image']
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title of your blog here'}),
            'blog_genre' : forms.Select(attrs={'class':'form-control'}),
            'blog_thumbnail':forms.FileInput(attrs={'class':'form-control'}),
            'blog_image':forms.FileInput(attrs={'class':'form-control'})
        }

class UpdateBlogForm(ModelForm):
    # title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title of your blog here'}))
    # # blog_genre' : forms.Select(attrs={'class':'form-control', 'placeholder':'Select a genre for the blog'}),
    # # tag' : forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Add tags'}),
    # blog_image = forms.MultipleChoiceField(widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta:
        model = Blog
        fields = ['title','description','blog_genre','tag','blog_thumbnail','blog_image']
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title of your blog here'}),
            'blog_genre' : forms.Select(attrs={'class':'form-control'}),
            'tag' : forms.SelectMultiple(attrs={'class':'form-control'}),
            'blog_thumbnail':forms.FileInput(attrs={'class':'form-control'}),
            'blog_image':forms.FileInput(attrs={'class':'form-control'})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message']