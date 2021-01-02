from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        # List comprehension make tuple of id / friendly name in categories
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # Put friendly names into the category.choices
        self.fields['category'].choices = friendly_names

        # Itterate through fields
        for field_name, field in self.fields.items():
            # Add class attributes to each field
            field.widget.attrs['class'] = 'border-black rounded-0'