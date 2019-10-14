# Generated by Django 2.2.3 on 2019-07-20 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allowance', '0004_registrationcodes'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationCodeToUsers',
            fields=[
                ('code', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('users', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserToRegistrationCode',
            fields=[
                ('user', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='RegistrationCodes',
        ),
    ]
