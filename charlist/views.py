from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView

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
        context["abilities"] = ["strength","constitution","dexterity","intelligence","wisdom","charisma"]
        context["skills"] = ["acrobatic","arcana","athletic","bluff","diplomacy",
                             "dungeoning","endurange","heal","history","insight",
                             "intimidate","nature","perception","religion","stealth",
                             "streetwise","thievery"]
        # Сюда бы еще добавить на чем эти скилы депендент, но мне впадлу
        context["senses"] = ["insight","perception"]
        context['user_value']=user_value
        return context

# Also hardcoded af, still waiting for models
user_value["sessions"] = ["eberron", "test_sesh", "dm_testing"]

class SessionSelection(TemplateView):
    template_name = "charlist/SessionSelection.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_value']=user_value
        return context

