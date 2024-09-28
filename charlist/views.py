from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView

# Hard coded af, waiting for xdmav
class CharListStats(TemplateView):
    template_name = "charlist/CharListStats.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["abilities"] = ["Strength","Constitution","Dexterity","Intelligence","Wisdom","Charisma"]
        context["senses"] = ["Insight","Perception"]
        return context
