from .models import User, ProfileImage
from django import forms


class AccountInformationEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name',
            'bio', 'birthday', 'country', 'state', 'city', 'address'
        )


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image_file']
