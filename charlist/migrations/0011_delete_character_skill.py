# Generated by Django 5.1.1 on 2024-10-07 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charlist', '0010_remove_character_bonus_initiative_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Character_Skill',
        ),
    ]