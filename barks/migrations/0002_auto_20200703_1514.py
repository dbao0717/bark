# Generated by Django 2.2 on 2020-07-03 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bark',
            options={'ordering': ['-id']},
        ),
    ]
