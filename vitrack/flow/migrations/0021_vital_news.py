# Generated by Django 4.0.2 on 2022-03-29 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0020_habits_alter_patientreport_report_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='vital',
            name='news',
            field=models.IntegerField(default=100),
        ),
    ]