from typing import Any
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db import transaction
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
import re

from .constants import (
    ACCESS_ERROR_MESSAGE,
    ALREAD_LOGGED_IN_USER_ERROR,
    DEFENSE_LABELS,
    INVALID_INVITATION_KEY_ERROR_MESSAGE,
    NON_EXISTENT_CHARACTER_ERROR,
    POST_REQUEST_ERROR_MESSAGE,
    USER_VALUE,
    SKILL_DEPENDENCIES,
)
from .forms import GeneralCharacteristicsForm, DefensesForm, MODEL_FORM_MAP
from .models import (
    Ability,
    Character,
    Character_Ability,
    Character_Health,
    Session,
    Session_GM,
    Session_Invitation,
    Session_User,
    Skill,
    Character_Defenses_Extra,
    CharList_Update,
)

from django.http import JsonResponse




# DRY this two ?
# Also they are very dependent on session_id being
def user_is_in_session(user, session: Session | int) -> bool:
    if user.is_anonymous:
        return False
    user_is_gm = Session_GM.objects.filter(Q(gm=user) & Q(session=session)).exists()
    user_is_player = Session_User.objects.filter(
        Q(user=user) & Q(session=session)
    ).exists()
    return user_is_gm | user_is_player
class SessionAccessRequiredMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        session_id = kwargs.get("session_id")
        if not user_is_in_session(request.user, session_id):
            return HttpResponseForbidden(ACCESS_ERROR_MESSAGE)
        return super().dispatch(request, *args, **kwargs)


def session_access_required(function=None):
    def wrapper(request, *args, **kwargs):
        user = request.user
        session = kwargs.get("char_id")
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
    except KeyError:
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
    except Session.DoesNotExist:
        return HttpResponse(INVALID_INVITATION_KEY_ERROR_MESSAGE)
    current_user = request.user

    if user_is_in_session(current_user, session):
        return HttpResponse(ALREAD_LOGGED_IN_USER_ERROR)
    else:
        Session_User.objects.create(session=session, user=current_user)
        return HttpResponseRedirect(
            reverse(
                "charlist:CharSelector",
                kwargs={
                    "session_id": session.id,
                },
            )
        )


class SessionSelection(LoginRequiredMixin, TemplateView):
    template_name = "charlist/SessionSelection.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        cur_user = self.request.user
        context = super().get_context_data(**kwargs)
        sessions = Session.objects.filter(
            Q(session_gm__gm=cur_user) | Q(session_user__user=cur_user)
        ).distinct()    
        session_data = []
        for session in sessions:
            try:
                invitation = Session_Invitation.objects.get(session=session)
            except Session_Invitation.DoesNotExist:
                invitation = Session_Invitation.objects.create(session=session)

            session_data.append(
                {
                    "info": session,
                    "invite_link": self.request.build_absolute_uri(
                        reverse(
                            "charlist:JoinSession",
                            kwargs={"invitation_key": invitation.key},
                        )
                    ),
                }
            )
        context["sessions"] = session_data
        return context


class CharSelector(SessionAccessRequiredMixin, TemplateView):
    template_name = "charlist/CharSelector.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        current_user = self.request.user
        context = super().get_context_data(**kwargs)
        context["characters"] = Character.objects.filter(
            Q(user=current_user.id) & Q(session__id=context["session_id"])
        )
        return context


class CharCreator(SessionAccessRequiredMixin, TemplateView):
    template_name = "charlist/CharCreator.html"


@session_access_required
def add_char(request, session_id):
    try:
        char_name = request.POST["name"]
    except KeyError:
        return HttpResponse(POST_REQUEST_ERROR_MESSAGE)
    else:
        current_user = request.user
        current_session = Session.objects.get(id=session_id)
        new_character = Character.objects.create(
            session=current_session, user=current_user, name=char_name
        )
        Character_Health.objects.create(character=new_character)
        for ability in Ability.objects.all():
            Character_Ability.objects.create(character=new_character, ability=ability)

        return HttpResponseRedirect(
            reverse(
                "charlist:CharListStats",
                kwargs={"session_id": session_id, "char_id": new_character.id},
            )
        )


class CharListStats(SessionAccessRequiredMixin, TemplateView):
    template_name = "charlist/CharListStats.html"

    def get(self, request, *args, **kwargs):
        session_id = self.kwargs.get("session_id")
        char_id = self.kwargs.get("char_id")
        user = self.request.user
        char_is_in_session = Character.objects.filter(
            session_id=session_id,
            user_id=user,  # we need to check if this char belongs to user
            pk=char_id,
        ).exists()
        if not char_is_in_session:  # crazy helpful repsonse...
            return HttpResponseForbidden(NON_EXISTENT_CHARACTER_ERROR)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        character = Character.objects.get(pk=self.kwargs.get("char_id"))
        context = super().get_context_data(**kwargs)
        context["character_id"] = character.id

        defense_data = Character_Defenses_Extra.objects.filter(character=character)
        context["defenses_form"] = DefensesForm(initial={
            'armor_coefficient': defense_data.first().armor_coefficient if defense_data.exists() else 0,
            'fortitude': defense_data.first().fortitude if defense_data.exists() else 0,
            'reflex': defense_data.first().reflex if defense_data.exists() else 0,
            'will': defense_data.first().will if defense_data.exists() else 0,
        })
        context["character_sheet_form"] = GeneralCharacteristicsForm(
            initial={
                "name": character.name,
                "char_class": character.char_class,
                "race": character.race,
                "xp": character.xp,
                "size": character.size,
                "gender": character.gender,
                "height": character.height,
                "weight": character.weight,
                "alignment": character.alignment,
                "deity": character.deity,
                "speed": character.speed,
                "action_points": character.action_points,
            }
        )

        character_abilities = Character_Ability.objects.filter(character_id=character.id)
        # Преобразуем ключи в строки (имена способностей)
        abilities_data = {
            str(ability.ability): ability.score for ability in character_abilities
        }
        skills = [str(skill) for skill in Skill.objects.all()]
        print(abilities_data)  # Для отладки
        context["abilities_data"] = abilities_data
        context["abilities"] = Ability.objects.values_list("ability", flat=True)

        context["skills"] = skills
        context["senses"] = ["insight", "perception"]
        context["defense_labels"] = DEFENSE_LABELS
        context["user_value"] = USER_VALUE
        context["session_id"] = self.kwargs.get("session_id")
        context["character_name"] = character.name
        context["skill_dependencies"] = SKILL_DEPENDENCIES

        return context

def create_charlist_update(user,char_id: int):
    updates = CharList_Update.objects.filter(user=user, character_id=char_id)
    if updates.count() > 100:
        with transaction.atomic():
            updates.delete()
        
    CharList_Update.objects.create(
        user=user,
        character=Character.objects.get(pk=char_id),
    )

def save_model_form_data(request, model_form_name):
    form_class = MODEL_FORM_MAP.get(model_form_name)
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            session_id = request.POST.get("session_key")
            session = Session.objects.get(pk=session_id)
            form.instance.session = session
            form.instance.user = request.user
            character_id = request.POST.get("character_id")
            character = Character.objects.filter(
                id=character_id
            ).first()
            if model_form_name == "DefensesForm":
                defense_extra, created = Character_Defenses_Extra.objects.get_or_create(
                    character=character,
                )
                for field, value in form.cleaned_data.items():
                    setattr(defense_extra, field, value)
                
                defense_extra.save()
            else:
                for field, value in form.cleaned_data.items():
                    setattr(character, field, value)
                character.save()

            create_charlist_update(request.user,character.pk)
            return JsonResponse({"message": "Data saved successfully!"})
    return JsonResponse({"error": "Invalid request method."}, status=405)

def save_handwritten_form_data(request, model_form_name):
    if request.method == "POST":
        data = request.POST
        print(data, model_form_name)
        character_id = int(request.POST.get("character_id"))
        character = get_object_or_404(Character, id=character_id)

        if model_form_name == 'abilities':
            # Фильтруем только способности, исключая те, которые содержат "mod" или "mod-plus"
            abilities = [item for item in data if item not in ('csrfmiddlewaretoken', 'session_key', 'user', 'character_id') and not re.search(r'(mod|mod-plus)', item)]
            for ability in abilities:
                score = data.get(ability)
                print(score)
                if not score:
                    continue

                score = int(score)
                modifier = (score - 10) // 2
                print("_________________")
                try:
                    ability_obj = Ability.objects.get(ability=ability)
                except Ability.DoesNotExist:
                    return JsonResponse({"error": f"Ability {ability} not found."}, status=404)

                # Сохраняем данные в модель Character_Ability
                try:

                    # Получаем или создаем запись о способности персонажа
                    character_ability, created = Character_Ability.objects.get_or_create(character_id=character.id, ability_id=ability_obj)

                    character_ability.score = score
                    character_ability.save()  # Сохраняем обновленную информацию

                except Exception as e:
                    return JsonResponse({"error": f"Error saving ability data: {str(e)}"}, status=500)

            # Отправляем успешный ответ
            create_charlist_update(request.user,character.pk)
            return JsonResponse({"message": "Data saved successfully!"})

    return JsonResponse({"error": "Invalid request method."}, status=405)

def long_poll(request: HttpRequest,char_id):
    update = CharList_Update.objects.filter(
        character = char_id
    ).order_by('-updated_at').first()
    last_updated_at = request.GET.get("last_updated_at")
    db_update = update.updated_at.strftime('%Y-%m-%dT%H:%M:%S')
    
    if db_update==last_updated_at[:19]:
        return JsonResponse({"status": "No update"})
    else:
        new_data = {}
        character_abilities = Character_Ability.objects.filter(character_id=char_id)
        abilities_data = {
            str(ability.ability): ability.score for ability in character_abilities
        }
        new_data["abilities"] = list(Ability.objects.values_list("ability", flat=True))#DANGEROUS  distinct flag may become disregarded
        new_data["ability_data"]=abilities_data

        defense_data = Character_Defenses_Extra.objects.filter(character_id = char_id)
        new_data["defenses"] = {
            'armor_coefficient': defense_data.first().armor_coefficient if defense_data.exists() else 0,
            'fortitude': defense_data.first().fortitude if defense_data.exists() else 0,
            'reflex': defense_data.first().reflex if defense_data.exists() else 0,
            'will': defense_data.first().will if defense_data.exists() else 0,
        }
        character = Character.objects.get(id = char_id)
        new_data["character"] = {
                "name": character.name,
                "char_class": character.char_class,
                "race": character.race,
                "xp": character.xp,
                "size": character.size.__str__(),
                "gender": character.gender.__str__(),
                "height": character.height,
                "weight": character.weight,
                "alignment": character.alignment,
                "deity": character.deity,
                "speed": character.speed,
                "action_points": character.action_points,
            }
        return JsonResponse({
            "status": "Success",
            "updated_at": update.updated_at,
            "new_data" : new_data,
        })

    
