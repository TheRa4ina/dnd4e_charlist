from typing import Iterable
from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
class Session(models.Model):
    def __str__(self):
        return f"{self.name}"
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Session_User")
    name = models.CharField(max_length=200)

class Session_Invitation(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    key = models.CharField(max_length=128,unique=True)

    def save(self, *args, **kwargs) -> None:
        if not self.key:
            self.key=self.generate_secret_key()
        super().save(*args,**kwargs)

    def generate_secret_key(self):
        return get_random_string(128)

class Session_User(models.Model):
    def __str__(self):
        return f"{self.session} - {self.user}"
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Session_GM(models.Model):
    def __str__(self):
        return f"{self.session} - {self.gm}"
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    gm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Gender(models.Model):
    def __str__(self):
        return self.gender
    gender = models.CharField(max_length=50, primary_key=True)

class Size(models.Model):
    def __str__(self):
        return self.size
    size = models.CharField(max_length=50, primary_key=True)

class Character(models.Model):
    def __str__(self):
        return self.name
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    char_class = models.CharField(max_length=200, null=True)
    race = models.CharField(max_length=200, null=True)
    xp = models.IntegerField(default=0)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,default="medium")
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE,default="male")
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    alignment = models.CharField(max_length=200, null=True)
    deity = models.CharField(max_length=200, null=True)
    speed = models.IntegerField(default=0)
    action_points = models.IntegerField(default=0)

class Character_Health(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE)
    max_hp = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    temp_hp = models.IntegerField(default=0)
    surges_day = models.IntegerField(default=0)
    surges_left = models.IntegerField(default=0)
    surges_bonus = models.IntegerField(default=0)

class Ability(models.Model):
    def __str__(self):
        return self.ability
    ability = models.CharField(max_length=200, primary_key=True)

class Skill(models.Model):
    def __str__(self):
        return self.skill
    skill = models.CharField(max_length=200, primary_key=True)
    
class Character_Ability(models.Model):
    def __str__(self):
        return f"{self.character}.{self.ability} = {self.score}"
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    score = models.IntegerField(default=10)

class Character_Defenses_Extra(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    extra_name = models.CharField(max_length=50)
    armor_coefficient = models.IntegerField(default=0)
    fortitude = models.IntegerField(default=0)
    reflex = models.IntegerField(default=0)
    will = models.IntegerField(default=0)

class Character_Initiative_Extra(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    extra_name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)

class Character_Speed_Extra(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    extra_name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)

class Character_Skill_Extra(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    extra_name = models.CharField(max_length=50)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

class Character_Trained_Skill(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

class Character_Notes(models.Model):
    def __str__(self):
        return f"{self.character}'s note: {self.note_name}"
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    note_name = models.CharField(max_length=100)
    note = models.TextField()

class Gm_Notes(models.Model):
    def __str__(self):
        return f"{self.gm}'s note: {self.note_name}"
    gm = models.ForeignKey(Session_GM, on_delete=models.CASCADE)
    note_name = models.CharField(max_length=100)
    note = models.TextField()
