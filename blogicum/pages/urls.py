from django.urls import path

from .views import TemplateAboutView, TemplateRulesView

app_name = 'pages'

urlpatterns = [
    path('about/', TemplateAboutView.as_view(), name='about'),
    path('rules/', TemplateRulesView.as_view(), name='rules'),
]
