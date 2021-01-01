from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """ Add placeholders and classes, remove auto generated labels amd set autofocus on first field """
        super().__init__(*args, **kwargs)
        # Create placeholders for form fields
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_town_or_city': 'Town or City',
            'default_county': 'County, State or Locality',
            'default_postcode': 'Post Code',
        }

        # Auto focus on full name field
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True

        # Itterate through fields adding a * if field is required
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]

            # Set placeholder to field
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Add class to field
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            # Remove form field labels
            self.fields[field].label = False