# Generated by Django 5.0.2 on 2024-02-08 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_alter_group_members'),
        ('users', '0005_customuser_pfp'),
    ]

    operations = [
        migrations.AddField(
            model_name='kick',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='kick_group', to='groups.group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kick',
            name='vote_needed',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
