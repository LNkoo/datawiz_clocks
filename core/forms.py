from django import forms
from django.contrib.auth.models import User

from core.models import Consumer


class ConsumerRegistrationForm(forms.ModelForm):
    login = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Consumer
        fields = (
            'login', 'email', 'password', 'name', 'surname', 'phone'
        )

    def save(self, commit=True):
        consumer = super().save(commit=False)
        if commit is True:
            account = User.objects.create(
                login=self.cleaned_data.get('login'),
                email=self.cleaned_data.get('email'),
                password=self.cleaned_data.get("password")
            )
            consumer.account = account
            consumer.save()
        return consumer
