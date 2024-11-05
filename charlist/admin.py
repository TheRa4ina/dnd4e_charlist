from typing import Any
from django.contrib import admin
from .models import *


class CharacterAbilityInline(admin.TabularInline):
    model = Character_Ability
    extra = 6  # Number of empty forms to display for new entries


class CharacterHealthInline(admin.StackedInline):
    model = Character_Health
    extra = 1


class CharacterDefensesExtraInline(admin.TabularInline):
    model = Character_Defenses_Extra
    extra = 1


class CharacterInitiativeExtraInline(admin.TabularInline):
    model = Character_Initiative_Extra
    extra = 1


class CharacterSpeedExtraInline(admin.TabularInline):
    model = Character_Speed_Extra
    extra = 1


class CharacterSkillExtraInline(admin.TabularInline):
    model = Character_Skill_Extra
    extra = 1


class CharacterTrainedSkillInline(admin.TabularInline):
    model = Character_Trained_Skill
    extra = 1


class CharacterNotesInline(admin.StackedInline):
    model = Character_Notes
    extra = 1


class CharacterAdmin(admin.ModelAdmin):
    fields = (
        'session', 'user', 'name', 'char_class', 'race', 'xp', 'size',
        'gender', 'height', 'weight', 'alignment', 'deity', 'speed', 'action_points'
    )
    list_display = ('name', 'char_class', 'race', 'xp')
    search_fields = ('name', 'char_class', 'race')

    inlines = [
        CharacterAbilityInline,
        CharacterHealthInline,
        CharacterDefensesExtraInline,
        CharacterInitiativeExtraInline,
        CharacterSpeedExtraInline,
        CharacterSkillExtraInline,
        CharacterTrainedSkillInline,
        CharacterNotesInline,
    ]


# Register the Character model with the custom admin class
admin.site.register(Character, CharacterAdmin)


class SessionUserInline(admin.TabularInline):
    model = Session_User
    extra = 1


class SessionGMInline(admin.TabularInline):
    model = Session_GM
    extra = 1


class SessionAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [
        SessionUserInline,
        SessionGMInline,
    ]


# Register the Session model with the custom admin class
admin.site.register(Session, SessionAdmin)
