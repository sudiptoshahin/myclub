# Generated by Django 5.1 on 2024-09-10 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='owner',
            field=models.IntegerField(default=1, verbose_name='Venue Owner'),
        ),
    ]
