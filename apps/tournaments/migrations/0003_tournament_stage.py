# Generated by Django 3.1.3 on 2020-11-14 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_tournament_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='stage',
            field=models.CharField(choices=[('PREPARATION', 'Preparation'), ('GROUP_STAGE', 'Group Stage'), ('QUARTER_FINAL', 'Quarter Final'), ('SEMI_FINAL', 'Semi Final'), ('FINAL', 'Final')], db_index=True, default='PREPARATION', max_length=20),
        ),
    ]
