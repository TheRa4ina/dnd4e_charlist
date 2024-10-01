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

class Gender(models.Model):
    gender = models.CharField(max_length=50,primary_key=True)

class Size(models.Model):
    size = models.CharField(max_length=50,primary_key=True)

class Character(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    char_class = models.CharField(max_length=200, null=True)
    race = models.CharField(max_length=200, null=True)
    xp = models.IntegerField(default=0)
    # SIZES = {
    #     "T": "Tiny",
    #     "S": "Small",
    #     "M": "Medium",
    #     "L": "Large",
    #     "H": "Huge",
    #     "G": "Gargantuan",
    # }
    size = models.ForeignKey(Size)
    gender = models.ForeignKey(Gender)
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
    ability = models.CharField(max_length=200,primary_key=True)

class Skills(models.Model):
    skill = models.CharField(max_length=200,primary_key=True)

class Character_Ability(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    ability = models.ForeignKey(Abilities,on_delete=models.CASCADE)
    score = models.IntegerField(default=10)

class Character_Skills(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills,on_delete=models.CASCADE)
    score=models.IntegerField(default=10)
    trained=models.BooleanField(default=False)


class Character_Defenses_Extra(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    extra_name = models.CharField(max_length=50)
    armor_coefficient = models.IntegerField(default=0)
    fortres = models.IntegerField(default=0)
    reflex = models.IntegerField(default=0)
    will = models.IntegerField(default=0)

class Character_Initiative_Extra(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    extra_name = models.CharField(max_length=50)
    score=models.IntegerField(default=0)

class Character_Trained_Skills(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)

class Character_Notes(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    note_name=models.CharField(max_length=100)
    note = models.CharField(max_length=2000)