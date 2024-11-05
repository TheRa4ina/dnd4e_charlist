from django import forms

from .models import Character, Character_Defenses_Extra


class GeneralCharacteristicsForm(forms.ModelForm):

    class Meta:
        model = Character
        exclude = ['session', 'user',]


class DefensesForm(forms.ModelForm):

    class Meta:
        model = Character_Defenses_Extra
        exclude = ['character', 'extra_name',]
