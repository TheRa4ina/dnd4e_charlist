from django import forms

from .models import Character, Character_Defenses_Extra



class GeneralCharacteristicsForm(forms.ModelForm):

    class Meta:
        model = Character
        exclude = ['session', 'user',]

    def __str__(self):
        return f"{self.__class__.__name__}"


class DefensesForm(forms.ModelForm):

    class Meta:
        model = Character_Defenses_Extra
        exclude = ['character', 'extra_name',]
    
    def __str__(self):
        return f"{self.__class__.__name__}"

MODEL_FORM_MAP = {
    'GeneralCharacteristicsForm': GeneralCharacteristicsForm,
    'DefensesForm': DefensesForm,
}