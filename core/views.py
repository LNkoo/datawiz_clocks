from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from core.forms import ConsumerRegistrationForm


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
            else:
                raise IntegrityError
        except IntegrityError:
            return render(
                request, self.template_name,
                {'errors': form.errors, 'form': form}
            )
        return redirect('departments')