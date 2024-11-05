from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView

from .constants import (
    ACCESS_ERROR_MESSAGE,
    ALREAD_LOGGED_IN_USER_ERROR,
    DEFENSE_LABELS,
    INVALID_INVITATION_KEY_ERROR_MESSAGE,
    NON_EXISTENT_CHARACTER_ERRROR,
    POST_REQUEST_ERROR_MESSAGE,
    USER_VALUE,
)
from .forms import GeneralCharacteristicsForm,DefensesForm
from .models import (
    Ability,
    Character,
    Character_Ability,
    Character_Health,
    Session,
    Session_GM,
    Session_Invitation,
    Session_User,
    Skill
)



def user_is_in_session(user, session: Session | int) -> bool:
    if (user.is_anonymous):
        return False
    user_is_gm = Session_GM.objects.filter(
        Q(gm=user) & Q(session=session)).exists()
    user_is_player = Session_User.objects.filter(
        Q(user=user) & Q(session=session)).exists()
    return user_is_gm | user_is_player

# maybe i can DRY this session access, but i dunno how to make it not bloated


class SessionAccessRequiredMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        if not user_is_in_session(request.user, session_id):
            return HttpResponseForbidden(ACCESS_ERROR_MESSAGE)
        return super().dispatch(request, *args, **kwargs)


def session_access_required(function=None):
    def wrapper(request, *args, **kwargs):
        user = request.user
        session = kwargs.get('session_id')
        if not (user_is_in_session(user, session)):
            return HttpResponseForbidden(ACCESS_ERROR_MESSAGE)
        else:
            return function(request, *args, **kwargs)
    return wrapper


class SessionCreator(LoginRequiredMixin, TemplateView):
    template_name = "charlist/SessionCreator.html"


@login_required
def add_session(request: HttpRequest):
    try:
        session_name = request.POST["name"]
    except (KeyError):
        return HttpResponse(POST_REQUEST_ERROR_MESSAGE)
    else:
        current_user = request.user
        new_session = Session.objects.create(name=session_name)
        Session_GM.objects.create(session=new_session, gm=current_user)
        Session_Invitation.objects.create(session=new_session)
        return HttpResponseRedirect(reverse("charlist:SessionSelector"))


@login_required
def join_session(request: HttpRequest, invitation_key):
    try:
        session = Session.objects.get(session_invitation__key=invitation_key)
    except (Session.DoesNotExist):
        return HttpResponse(INVALID_INVITATION_KEY_ERROR_MESSAGE)
    current_user = request.user

    if (user_is_in_session(current_user, session)):
        return HttpResponse(ALREAD_LOGGED_IN_USER_ERROR)
    else:
        Session_User.objects.create(session=session, user=current_user)
        return HttpResponseRedirect(
            reverse(
                "charlist:CharSelector",
                kwargs={"session_id": session.id, }
            )
        )


class SessionSelection(LoginRequiredMixin, TemplateView):
    template_name = "charlist/SessionSelection.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        cur_user = self.request.user
        context = super().get_context_data(**kwargs)
        sessions = Session.objects.filter(
            Q(session_gm__gm=cur_user) | Q(session_user__user=cur_user)
        )
        session_data = []
        for session in sessions:
            try:
                invitation = Session_Invitation.objects.get(session=session)
            except Session_Invitation.DoesNotExist:
                invitation = Session_Invitation.objects.create(session=session)

            session_data.append({
                'info': session,
                'invite_link': self.request.build_absolute_uri(
                    reverse('charlist:JoinSession',
                                kwargs={'invitation_key': invitation.key}))
            })
        context["sessions"] = session_data
        return context


class CharSelector(SessionAccessRequiredMixin, TemplateView):
    template_name = "charlist/CharSelector.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        current_user = self.request.user
        context = super().get_context_data(**kwargs)
        context["characters"] = Character.objects.filter(
            Q(user=current_user.id) &
            Q(session__id=context['session_id'])
        )
        return context


class CharCreator(SessionAccessRequiredMixin, TemplateView):
    template_name = "charlist/CharCreator.html"


@session_access_required
def add_char(request, session_id):
    try:
        char_name = request.POST["name"]
    except (KeyError):
        return HttpResponse(POST_REQUEST_ERROR_MESSAGE)
    else:
        current_user = request.user
        current_session = Session.objects.get(id=session_id)
        new_character = Character.objects.create(
            session=current_session,
            user=current_user,
            name=char_name)
        Character_Health.objects.create(character=new_character)
        for ability in Ability.objects.all():
            Character_Ability.objects.create(
                character=new_character,
                ability=ability)

        return HttpResponseRedirect(
            reverse(
                "charlist:CharListStats",
                kwargs={"session_id": session_id, "char_id": new_character.id}
            )
        )


class CharListStats(SessionAccessRequiredMixin, TemplateView):
    template_name = "charlist/CharListStats.html"

    def get(self, request, *args, **kwargs):
        session_id = self.kwargs.get('session_id')
        char_id = self.kwargs.get('char_id')
        user = self.request.user
        char_is_in_session = Character.objects.filter(
            session_id=session_id,
            user_id=user,  # we need to check if this char belongs to user
            pk=char_id).exists()
        if not char_is_in_session:  # crazy helpful repsonse...
            return HttpResponseForbidden(NON_EXISTENT_CHARACTER_ERRROR)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["character_sheet_form"] = GeneralCharacteristicsForm()
        context["basis"] = ["name", "class", "race", "size", "age",
                            "gender", "height", "weight", "algnment",
                            "deity", "max-hp", "surges-day", "level"]
        context["abilities"] = Ability.objects.values_list(
            "ability", flat=True)  # flat, so it returns single values
        context["skills"] = Skill.objects.all()
        context["senses"] = ["insight", "perception"]
        context["defenses_form"] = DefensesForm()
        context["defense_labels"] = DEFENSE_LABELS
        context['user_value'] = USER_VALUE
        return context
