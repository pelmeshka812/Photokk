# Generated by Django 3.0.5 on 2020-05-28 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200519_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photodesk',
            name='desk',
        ),
        migrations.RemoveField(
            model_name='photodesk',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='userdesk',
            name='desk',
        ),
        migrations.RemoveField(
            model_name='userdesk',
            name='user',
        ),
        migrations.DeleteModel(
            name='Desk',
        ),
        migrations.DeleteModel(
            name='PhotoDesk',
        ),
        migrations.DeleteModel(
            name='UserDesk',
        ),
    ]
