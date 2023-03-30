# Generated by Django 4.0 on 2023-03-30 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.AlterField(
            model_name='payment',
            name='booking',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='flights.booking'),
        ),
    ]
