from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """ Add placeholders and classes, remove auto generated labels amd set autofocus on first field """
        super().__init__(*args, **kwargs)
        # Create placeholders for form fields
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'county': 'County, State or Locality',
            'postcode': 'Post Code',
        }

        # Auto focus on full name field
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # Itterate through fields adding a * if field is required
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]

            # Set placeholder to field
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Add class to field
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Remove form field labels
            self.fields[field].label = False