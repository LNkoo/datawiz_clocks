from django.views.generic import TemplateView


class DepartmentView(TemplateView):
    template_name = 'core/department.html'