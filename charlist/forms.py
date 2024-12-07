from django import forms

from .models import Character, Character_Defenses_Extra



class GeneralCharacteristicsForm(forms.ModelForm):

    class Meta:
        model = Character
        exclude = ['session', 'user',]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['deity'].required = False
        self.fields['alignment'].required = False
        self.fields['race'].required = False
        self.fields['char_class'].required = False

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