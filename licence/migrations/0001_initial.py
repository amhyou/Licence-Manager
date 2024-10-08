# Generated by Django 5.1.1 on 2024-09-19 14:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Licence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued_date', models.DateField()),
                ('expiration_date', models.DateField()),
                ('key', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('expired', 'Expired'), ('revoked', 'Revoked')], default='active', max_length=10)),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_login', models.DateTimeField()),
                ('last_login', models.DateTimeField()),
                ('mac', models.CharField(max_length=17, unique=True)),
                ('device_name', models.CharField(blank=True, max_length=100, null=True)),
                ('licence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='licence.licence')),
            ],
        ),
    ]
