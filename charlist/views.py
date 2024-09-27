from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class CharListStats(TemplateView):
    template_name = "charlist/CharListStats.html"
    