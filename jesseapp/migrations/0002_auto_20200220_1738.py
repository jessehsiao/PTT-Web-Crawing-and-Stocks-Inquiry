# Generated by Django 3.0.3 on 2020-02-20 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jesseapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='userID',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='userid',
            new_name='userID',
        ),
    ]
