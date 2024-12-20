from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'photo', 'publish', 'status', 'tags']  # Include 'publish' field

    # You can also apply additional customizations if needed, like widgets for styling
    publish = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Display datetime in a local input format
        required=True
    )