# Generated by Django 4.0 on 2023-03-25 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_passenger_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger',
            name='name',
            field=models.CharField(default='sid', max_length=100),
            preserve_default=False,
        ),
    ]
