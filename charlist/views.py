from typing import Any
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,HttpRequest
from django.views.generic.base import TemplateView
from django.core import exceptions
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
        Session_GM.objects.create(session=new_session,gm=current_user)
        Session_Invitation.objects.create(session = new_session)
        return HttpResponseRedirect(reverse("charlist:SessionSelector"))
    
def join_session(request: HttpRequest,invitation_key):
    try:
        session = Session.objects.get(session_invitation__key = invitation_key)
    except(Session_Invitation.DoesNotExist):
        return HttpResponse("Invalid invitation key")
    current_user = request.user
    user_is_gm = Session_GM.objects.filter(Q(gm = current_user) & Q(session=session)).exists()
    user_is_player = Session_User.objects.filter(Q(user = current_user) & Q(session = session)).exists()
    user_already_in = user_is_gm | user_is_player

    if(user_already_in):
        return HttpResponse("You are already in this session")
    else:
        Session_User.objects.create(session=session,user=current_user)
        return HttpResponseRedirect(reverse("charlist:CharSelector",kwargs={
            "session_id" : session.id,
            }))
    

class SessionSelection(LoginRequiredMixin,TemplateView):
    login_url="admin/"
    template_name = "charlist/SessionSelection.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        cur_user = self.request.user
        context = super().get_context_data(**kwargs)
        sessions = Session.objects.filter(
            Q(session_gm__gm = cur_user) | Q(session_user__user = cur_user)
            )
        session_data = []
        for session in sessions:
            try:
                invitation = Session_Invitation.objects.get(session=session)
            except Session_Invitation.DoesNotExist:
                invitation = Session_Invitation.objects.create(session = session)

            session_data.append({
                    'info': session,
                    'invite_link': self.request.build_absolute_uri(
                        reverse('charlist:JoinSession',
                                 kwargs={'invitation_key': invitation.key}))
                })

        
        context["sessions"]=session_data
        return context
    

    
class CharSelector(TemplateView):
    template_name= "charlist/CharSelector.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        current_user = self.request.user
        context = super().get_context_data(**kwargs)
        context["characters"] = Character.objects.filter(
            Q(user=current_user.id) &
            Q(session__id=context['session_id'])
            )
        return context
    
class CharCreator(TemplateView):
    template_name="charlist/CharCreator.html"

def add_char(request,session_id):
    try:
        char_name = request.POST["name"]
    except(KeyError):
        return HttpResponse("Invalid post")
    else:
        current_user = request.user
        current_session = Session.objects.get(id = session_id)    
        new_character = Character.objects.create(
            session=current_session,
            user = current_user,
            name = char_name)
        Character_Health.objects.create(character=new_character)
        for ability in Ability.objects.all():
            Character_Ability.objects.create(
                character = new_character,
                ability = ability)
        
        return HttpResponseRedirect(reverse("charlist:CharListStats",kwargs={
            "session_id":session_id,
            "char_id":new_character.id
        }))

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
    





