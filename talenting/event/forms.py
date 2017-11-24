from django import forms

from .models import Event, EventComment


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = (
            'title',
            'program',
            'noted_item',
            'country',
            'state',
            'city',
            'price',
            'photo',
            'starting_date',
            'closing_date',
            'maximum_participant',
        )

    def save(self, commit=True, *args, **kwargs):
        if not self.instance.pk and commit:
            author = kwargs.pop('author', None)
            if not author:
                raise ValueError('Author field is required')
            self.instance.author = author
        return super().save(*args, **kwargs)


class CommentForm(forms.ModelForm):

    class Meta:
        model = EventComment
        fields = (
            'content',
        )
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }

