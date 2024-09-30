from django.db import models
from django.conf import settings

class Game(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Game_Users")
    name = models.CharField(max_length=200)

class Game_Users(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Game_GMs(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    gm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Character(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    char_class = models.CharField(max_length=200, null=True)
    race = models.CharField(max_length=200, null=True)
    xp = models.IntegerField(default=0)
    SIZES = {
        "T": "Tiny",
        "S": "Small",
        "M": "Medium",
        "L": "Large",
        "H": "Huge",
        "G": "Gargantuan",
    }
    size = models.CharField(max_length=1, choices=SIZES, default="M")
    GENDERS = {
        "M": "Male",
        "F": "Female",
        "O": "Other",
    }
    gender = models.CharField(max_length=1, choices=GENDERS, default="M")
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    alignment = models.CharField(max_length=200, null=True)
    deity = models.CharField(max_length=200, null=True)
    speed = models.IntegerField(default=0)
    action_points = models.IntegerField(default=0)
    bonus_initiative = models.IntegerField(default=0)

class Character_Health:
    character = models.OneToOneField(Character, on_delete=models.CASCADE)
    max_hp = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    temp_hp = models.IntegerField(default=0)
    surges_day = models.IntegerField(default=0)

class Abilities(models.Model):
    ability = models.CharField(max_length=200)

class Skills(models.Model):
    skill = models.CharField(max_length=200)

class Character_Ability:
    character = models.OneToOneField(Character, on_delete=models.CASCADE)
    strength = models.IntegerField(default=0)
    constitution = models.IntegerField(default=0)
    dexterity = models.IntegerField(default=0)
    intelligence = models.IntegerField(default=0)
    wisdom = models.IntegerField(default=0)
    charisma = models.IntegerField(default=0)

class Character_Skills:
    character = models.OneToOneField(Character, on_delete=models.CASCADE)
    arcana = models.IntegerField(default=0)
    athletic = models.IntegerField(default=0)
    bluff = models.IntegerField(default=0)
    diplomacy = models.IntegerField(default=0)
    dungeoning = models.IntegerField(default=0)
    endurange = models.IntegerField(default=0)
    heal = models.IntegerField(default=0)
    history = models.IntegerField(default=0)
    insight = models.IntegerField(default=0)
    intimidate = models.IntegerField(default=0)
    nature = models.IntegerField(default=0)
    perception = models.IntegerField(default=0)
    religion = models.IntegerField(default=0)
    stealth = models.IntegerField(default=0)
    streetwise = models.IntegerField(default=0)
    thievery = models.IntegerField(default=0)

class Character_Defenses:
    character = models.OneToOneField(Character, on_delete=models.CASCADE)
    armor_coefficient = models.IntegerField(default=0)
    fortres = models.IntegerField(default=0)
    reflex = models.IntegerField(default=0)
    will = models.IntegerField(default=0)

class Character_Trained_Skills:
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)

class Character_Notes:
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    note = models.CharField(max_length=2000)
