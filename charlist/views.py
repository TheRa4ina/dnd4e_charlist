from typing import Any
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,HttpRequest
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.urls import reverse
from django.db.models import Q

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
        context["basis"] = ["name","class","race","size","age",
                            "gender","height","weight","algnment",
                            "deity","max-hp","surges-day","level"]
        context["abilities"] = Ability.objects.values_list("ability",flat=True)#flat, so it returns single values
        context["skills"] = Skill.objects.all()
        context["senses"] = ["insight","perception"]
        context["defenses"] = ["armor_coefficient","fortitude","reflex","will"]
        context['user_value']=user_value
        return context
    

class CharCreator(TemplateView):
    template_name="charlist/CharCreator.html"

def add_char(request,session_name):
    try:
        char_name = request.POST["name"]
    except(KeyError):
        return HttpResponse("Invalid post")
    else:
        #char-creation-placeholder

        return HttpResponseRedirect(reverse("charlist:CharListStats",kwargs={
            "session_name":session_name,
        }))


class SessionSelection(LoginRequiredMixin,TemplateView):
    login_url="admin/"
    template_name = "charlist/SessionSelection.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        cur_user = self.request.user
        context = super().get_context_data(**kwargs)
        context["sessions"] = Session.objects.filter(Q(session_gm__gm = cur_user) | Q(session_user__user = cur_user))
        return context

class SessionCreator(TemplateView):
    template_name="charlist/SessionCreator.html"

def add_session(request: HttpRequest):
    try:
        session_name = request.POST["name"]
    except(KeyError):
        return HttpResponse("Invalid post")
    else:
        current_user = request.user
        new_session = Session.objects.create(name = session_name)
        new_session_gm = Session_GM.objects.create(session=new_session,gm=current_user)
        return HttpResponseRedirect(reverse("charlist:SessionSelector"))