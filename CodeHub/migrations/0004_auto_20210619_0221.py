# Generated by Django 2.2.24 on 2021-06-18 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CodeHub', '0003_cfid_cfusername'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cfid',
            name='mrank',
        ),
        migrations.RemoveField(
            model_name='cfid',
            name='mrating',
        ),
        migrations.RemoveField(
            model_name='cfid',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='cfid',
            name='rating',
        ),
    ]
