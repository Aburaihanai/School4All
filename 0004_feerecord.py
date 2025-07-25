# Generated by Django 5.2.3 on 2025-06-24 10:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_userprofile_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeeRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('term', models.CharField(max_length=100)),
                ('date_recorded', models.DateField(auto_now_add=True)),
                ('student', models.ForeignKey(limit_choices_to={'role': 'student'}, on_delete=django.db.models.deletion.CASCADE, to='users.userprofile')),
            ],
        ),
    ]
