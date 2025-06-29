import re

from django import forms

from app.messages import ERROR_MESSAGES
from orders.models import Order

class CreateOrderForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()
    requires_delivery = forms.ChoiceField(choices=[
        ("0", "False"),
        ("1", "True"),
    ])
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=[
        ("0", "False"),
        ("1", "True"),
    ])

    # def clean_phone(self):
    #     data = self.cleaned_data['phone']
    #
    #     if not data.isdigit():
    #         raise forms.ValidationError(ERROR_MESSAGES["incorrect_phone"])
    #
    #     pattern = re.compile(r"^\d[10]")
    #     if not pattern.match(data):
    #         raise forms.ValidationError(ERROR_MESSAGES["incorrect_phone"])
    #
    #     return data

    class Meta:
        model = Order
        fields = ['phone', 'requires_delivery', 'delivery_address', 'payment_on_get']