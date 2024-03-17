from django.views.generic import TemplateView


class TemplateAboutView(TemplateView):
    template_name = 'pages/about.html'


class TemplateRulesView(TemplateView):
    template_name = 'pages/rules.html'
