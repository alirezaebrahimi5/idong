# Generated by Django 5.0.2 on 2024-02-08 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='expense/group/'),
        ),
    ]
