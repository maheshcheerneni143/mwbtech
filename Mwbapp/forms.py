from django import forms
from .models import Add_Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Add_Product
        fields = '__all__'
        