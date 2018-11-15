from django.contrib.auth import login
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from core.forms import ConsumerRegistrationForm
from core.models import Consumer


class DepartmentView(TemplateView):
    template_name = 'core/department.html'

class ConsumerRegistrationView(TemplateView):
    template_name = 'core/registration.html'

    def get_context_data(self, **kwargs):
        return {'form': ConsumerRegistrationForm()}

    def post(self, request):
        form = ConsumerRegistrationForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                login(request, form.instance.account)
            else:
                raise IntegrityError
        except IntegrityError:
            return render(
                request, self.template_name,
                {'errors': form.errors, 'form': form}
            )
        return redirect('departments')

class ConsumerAutorizationView(TemplateView):
    template_name = 'core/authorization.html'
    def post(self,request):
        consumer = get_object_or_404(
            Consumer,
            account__username = request.POST.get('username'),
            account__password = request.POST.get('password'),
        )
        login(request, consumer.account)
        return redirect('departments')
