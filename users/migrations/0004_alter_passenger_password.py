# Generated by Django 4.0 on 2023-03-24 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_passenger_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]