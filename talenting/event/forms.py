from django import forms

from .models import Event, EventComment, Photo


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
            'primary_photo',
            'opening_date',
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


class ImageForm(forms.ModelForm):
    # this will return only first saved image on save()
    image = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}), required=True)

    class Meta:
        model = Photo
        fields = ['image', 'position']

    def save(self, *args, **kwargs):
        # multiple file upload
        # NB: does not respect 'commit' kwarg

        self.instance.image = file_list[0]
        for file in file_list[1:]:
            Photo.objects.create(
                product=self.cleaned_data['product'],
                image=file,
                position=self.cleaned_data['position'],
            )

        return super().save(*args, **kwargs)