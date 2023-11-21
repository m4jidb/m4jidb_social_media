from .models import User, ProfileImage
from django import forms
from allauth.account.forms import SignupForm


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


class CustomSignupForm(SignupForm):
    phone = forms.CharField(max_length=11, required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.phone = self.cleaned_data['phone']
        user.save()
        return user
