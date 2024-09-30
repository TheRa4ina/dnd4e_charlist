# Generated by Django 5.1.1 on 2024-10-04 07:54

from django.db import migrations

def populate_skills(apps,schema_editor):
    Skill = apps.get_model("charlist","Skill")
    skills = ["acrobatic","arcana","athletic","bluff","diplomacy",
              "dungeoning","endurange","heal","history","insight",
              "intimidate","nature","perception","religion","stealth",
              "streetwise","thievery"]
    skill_objects = [Skill(skill=skill) for skill in skills]
    Skill.objects.bulk_create(skill_objects)

def populate_abilites(apps,schema_editor):
    Ability = apps.get_model("charlist","Ability")
    abilities = ["strength","constitution","dexterity","intelligence","wisdom","charisma"]
    ability_objects = [Ability(ability=ability) for ability in abilities]
    Ability.objects.bulk_create(ability_objects)

def populate_genders(apps,schema_editor):
    Gender = apps.get_model("charlist","Gender")
    genders = ["male","female","other"]
    gender_objects = [Gender(gender=gender) for gender in genders]
    Gender.objects.bulk_create(gender_objects)
def populate_sizes(apps,schema_editor):
    Size = apps.get_model("charlist","Size")
    sizes = ["tiny","small","medium","large","huge","gargantuan"]
    size_objects = [Size(size=size) for size in sizes]
    Size.objects.bulk_create(size_objects)

class Migration(migrations.Migration):

    dependencies = [
        ('charlist', '0003_ability_character_ability_character_defenses_extra_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_skills),
        migrations.RunPython(populate_abilites),
        migrations.RunPython(populate_genders),

    ]