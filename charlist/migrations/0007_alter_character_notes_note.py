# Generated by Django 5.1.1 on 2024-10-04 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charlist', '0006_gm_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character_notes',
            name='note',
            field=models.TextField(),
        ),
    ]
