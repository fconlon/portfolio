# Generated by Django 2.1 on 2018-08-18 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survivors',
            fields=[
                ('pclass', models.IntegerField()),
                ('survived', models.BooleanField()),
                ('name', models.CharField(max_length=82, primary_key=True, serialize=False)),
                ('sex', models.CharField(max_length=6)),
                ('age', models.IntegerField()),
            ],
        ),
    ]
