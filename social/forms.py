from django import forms
from .models import Comment,  Post


class PostForm(forms.ModelForm):
    images = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'tags']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Add other fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your comment here'})
