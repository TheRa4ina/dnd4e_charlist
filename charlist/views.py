from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import *

# Hard coded af, waiting for xdmav's models
user_value = {
    'abilities' :{
        'strength': 12,
        'constitution' : 14,
        'dexterity' : 13,
        'intelligence' : 15,
        'wisdom' : 6,
        'charisma' : 17,
    }
}

class CharListStats(TemplateView):
    template_name = "charlist/CharListStats.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["abilities"] = Ability.objects.all()
        context["skills"] = Skill.objects.all()
        context["senses"] = ["insight","perception"]
        context["defenses"] = ["armor_coefficient","fortitude","reflex","will"]
        context['user_value']=user_value
        return context

# Still hardcoded asf
user_value["sessions"] = ["eberron", "test_sesh", "dm_testing"]

class SessionSelection(TemplateView):
    template_name = "charlist/SessionSelection.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_value']=user_value
        return context

