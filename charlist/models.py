from django.db import models
from django.conf import settings

class Game(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Game_User")
    name = models.CharField(max_length=200)

class Game_User(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Game_GM(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    gm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Gender(models.Model):
    def __str__(self) -> str:
        return self.gender
    gender = models.CharField(max_length=50,primary_key=True)

class Size(models.Model):
    def __str__(self) -> str:
        return self.size
    size = models.CharField(max_length=50,primary_key=True)

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
    surges_left = models.IntegerField(default=0)
    surges_bonus = models.IntegerField(default=0)

class Ability(models.Model):
    def __str__(self) -> str:
        return self.ability
    ability = models.CharField(max_length=200,primary_key=True)

class Skill(models.Model):
    def __str__(self) -> str:
        return self.skill
    skill = models.CharField(max_length=200,primary_key=True)

class Character_Ability(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability,on_delete=models.CASCADE)
    score = models.IntegerField(default=10)

class Character_Skill(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill,on_delete=models.CASCADE)
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

class Character_Skill_Extra(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    extra_name = models.CharField(max_length=50)
    skill = models.ForeignKey(Skill,on_delete=models.CASCADE)
    score=models.IntegerField(default=0)

class Character_Trained_Skill(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    
class Character_Notes(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    note_name=models.CharField(max_length=100)
    note_name=models.CharField(max_length=100)
    note = models.CharField(max_length=2000)


