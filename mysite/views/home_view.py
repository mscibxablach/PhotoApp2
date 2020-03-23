from django.views.generic import TemplateView, ListView, CreateView


class Home(TemplateView):
    template_name = 'home.html'
