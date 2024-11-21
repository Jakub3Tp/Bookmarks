from http.client import responses
from django import forms
from django.core.files.base import ContentFile
from django.template.context_processors import request
from django.template.defaultfilters import slugify

from images.models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("Podany url nie zawiera poprawnego rozszerzenia")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        extension = image_url.rsplit('.', 1)[1].lower()
        name = slugify(image.title)
        image_name = f'{name}.{extension}'

        response = request.get(image_url)
        image.image.save(image_name, ContentFile(response.content), save=False)

        if commit:
            image.save()

        return image