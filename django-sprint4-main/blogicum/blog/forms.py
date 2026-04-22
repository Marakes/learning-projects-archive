from django import forms

from blog.models import Comment, Post


class PostForm(forms.ModelForm):
    """Форма на основе модели поста."""

    class Meta:
        model = Post
        exclude = ('author',)

        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            )
        }


class CommentForm(forms.ModelForm):
    """Форма на основе модели комментария."""

    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(
                attrs={
                    'rows': 4,
                    'cols': 40,
                    'placeholder': 'Мэээн, напиши что-нибудь...',
                    'class': 'form-control',
                }
            )
        }
