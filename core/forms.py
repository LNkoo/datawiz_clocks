from django import forms
from django.contrib.auth.models import User

from core.models import Consumer, Basket


class ConsumerRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Consumer
        fields = (
            'username', 'email', 'password', 'name', 'surname', 'phone'
        )

    def save(self, commit=True):
        consumer = super().save(commit=False)
        if commit is True:
            account = User.objects.create(
                username=self.cleaned_data.get('username'),
                email=self.cleaned_data.get('email'),
                password=self.cleaned_data.get("password")
            )
            Basket.objects.create(consumer=consumer)
            consumer.account = account
            consumer.save()
        return consumer


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 51)]


class AddProductInBasket(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label="Кількість"
    )
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
