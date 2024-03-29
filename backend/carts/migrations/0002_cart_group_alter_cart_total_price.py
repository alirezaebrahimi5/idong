# Generated by Django 5.0.2 on 2024-02-10 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
        ('groups', '0004_kick_kickvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cart_group', to='groups.group'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
