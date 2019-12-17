from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['buyer', 'address']

        widgets = {
            'buyer': forms.TextInput(
                attrs={'class': 'form-control','style': 'width:300px; margin: 0 auto;'}
            ),
            'address': forms.TextInput(
                attrs={'class': 'form-control','style': 'width:300px; margin: 0 auto;'}
            )
        }